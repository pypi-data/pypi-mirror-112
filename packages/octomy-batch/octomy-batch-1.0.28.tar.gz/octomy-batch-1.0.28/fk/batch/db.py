import pytz

from fk.db.DatabaseConnection import DatabaseConnection


class Database:

    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    FAILED = "failed"

    def __init__(self, config):
        self.config = config
        self.dbc = DatabaseConnection.get_connection(self.config)
        assert self.dbc.is_ok()
        self.create_tables()

    def create_tables(self):

        # Create a table to keep track of batch items
        self.dbc.query_none(
            """
            create table if not exists "batch_log" (
                id serial primary key,
                priority int not null default 50,
                data text,
                result text,
                type varchar(255),
                status varchar(255),
                throttle_key varchar(63),
                throttle_limit integer,
                throttle_period integer, 
                source text,
                error text,
                created_at timestamptz not null default now(),
                updated_at timestamptz not null default now()
            );
            comment on column batch_log.id is 'Unique internal id for this batch item';
            comment on column batch_log.data is 'The batch item''s data. Depends entirely on the type. Could for example be the URL to scrape for a site_scrape item';
            comment on column batch_log.result is 'The batch item''s result data. Depends entirely on the type. Could for example be the HTML scraped for the input URL for a site_scrape item';
            comment on column batch_log.type is 'The batch item''s type such as order_scrape or site_scrape';
            comment on column batch_log.status is 'The batch item''s status such as pending, in-progress or done';
            comment on column batch_log.throttle_key is 'When set enables throttling between all items that have the same key';
            comment on column batch_log.throttle_limit is 'When throttle_key is set, this specifies the number of items that can be processed over throttle_period';
            comment on column batch_log.throttle_period is 'When throttle_key is set, this specifies the period over which throttle_limit items may be processed';
            comment on column batch_log.source is 'The batch item''s source. Spesifically which component registered it.';
            comment on column batch_log.error is 'The batch item''s error message. Should be None unless status is "failed", in which it case it should be a descriptive error message.';
            comment on column batch_log.created_at is 'When the batch item was first created';
            comment on column batch_log.updated_at is 'When the batch item was last updated';
            """
        )

        # Inspired by https://dev.to/astagi/rate-limiting-using-python-and-redis-58gk
        # Create a function to keep track of throttling of batch items
        # NOTE: Throttling works by an algorithm called Generic Cell Rate Algoritm (GCRA for short).
        #       The function is called for a key, and will return an integer number of milliseconds to wait for the key to become unlimited
        #       The function can be called with do_book=true to actually perform booking if the key is unlimited
        #       The parameters limit_count and period_millis are used to specify the limit where
        #       limit_count is the number of actions allowed over the time interval of period_millis
        self.dbc.query_none(
            """
-- function that returns the number of milliseconds to wait before the given throttle_key is available. If the value returned is <=0 that means you just got lucky and no throttle was necessary for that key at this point.
drop function if exists gcra_throttle (varchar, integer, integer, boolean);
create or replace function gcra_throttle (throttle_key varchar(63), limit_count integer, period_millis integer, do_book boolean) returns bigint as $$
declare
    -- Holds current time in milliseconds since epoch at the entry of the function
    now_millis bigint;
    -- Holds our current value of TAT in milliseconds since epoch
    tat_millis bigint;
    -- Holds the return value for "how long should we wait before invoking our throttled action?" in milliseconds
    left_millis bigint;
begin

    -- Trivial reject: when throttle_key is not set we return 0 to signify no rate limiting needed
    if (throttle_key = '') is not false then
        return 0;
    end if;

    -- Get current time in milliseconds since epoch
    select extract(epoch from now()) * 1000 into now_millis;
    
    -- Make sure our working table is ready
    create unlogged table if not exists throttle_tat(
        key varchar(63) primary key,
        millis bigint
    );

    -- Hold an exclusive lock on the table to avoid race conditions
    lock table throttle_tat in exclusive mode;

    -- Get stored value for tat, initializing it to 0 if it was not set 
    select t.millis into tat_millis from throttle_tat t where t.key = $1;
    if tat_millis is null then
        tat_millis := now_millis;
        insert into throttle_tat (key, millis) values ($1, tat_millis);
    end if;

    -- Calculate how many milliseconds we should wait before performing our action.
    -- NOTE: Zero or negative values means we don't need to wait
    left_millis := (tat_millis - now_millis)  -  (period_millis - (period_millis / limit_count));

    -- We waited long enough, perform our booking if so desired
    if do_book and left_millis <= 0 then
        update throttle_tat t set millis = greatest(tat_millis, now_millis) + (period_millis / limit_count) where t.key = $1;
    end if;
    return left_millis;
end
$$ language plpgsql;
""",
            [],
        )

    # Look at faster batch imports with
    # from psycopg2.extras import execute_values
    # execute_values(cur,
    # "INSERT INTO test (id, v1, v2) VALUES %s",
    # [(1, 2, 3), (4, 5, 6), (7, 8, 9)])
    # FROM https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query

    # Insert a new batch item into log
    def insert_batch_item(self, batch_item):
        return self.dbc.query_one(
            """
                insert into batch_log
                    (
                    priority,
                    data,
                    result,
                    type,
                    status,
                    throttle_key,
                    throttle_limit,
                    throttle_period,
                    source
                    )
                values
                    (
                    %(priority)s,
                    %(data)s,
                    %(result)s,
                    %(type)s,
                    %(status)s,
                    %(throttle_key)s,
                    %(throttle_limit)s,
                    %(throttle_period)s,
                    %(source)s
                    )
                on conflict(id)
                do update
                    set priority=%(priority)s,
                    data=%(data)s,
                    result=%(result)s,
                    type=%(type)s,
                    status=%(status)s,
                    throttle_key=%(throttle_key)s,
                    throttle_limit=%(throttle_limit)s,
                    throttle_period=%(throttle_period)s,
                    source=%(source)s,
                    updated_at=now()
                returning id
                ;
                """,
            batch_item,
        )

    # Update a batch item in the batch log, making sure to fail if the id and updated_at don't match, providing a guarantee of atomic operation
    # Returns updated_at, so caller can check if it was updated or not (compare it to argument)
    def update_batch_item(self, batch_item):
        return self.dbc.query_one(
            """
                update batch_log
                    set priority=%(priority)s,
                    data=%(data)s,
                    result=%(result)s,
                    type=%(type)s,
                    status=%(status)s,
                    throttle_key=%(throttle_key)s,
                    throttle_limit=%(throttle_limit)s,
                    throttle_period=%(throttle_period)s,
                    source=%(source)s,
                    error=%(error)s,
                    updated_at=now()
                where id = %(id)s
                and updated_at = %(updated_at)s
                returning updated_at
                ;
                """,
            batch_item,
        )

    # Update status of all jobs with from_status to to_status given they have time delta longer than given time
    def bump_batch_items(self, from_status=IN_PROGRESS, to_status=PENDING, time_sec=30):
        return self.dbc.query_none(
            """
                update batch_log
                    set
                    status=%(to_status)s,
                    updated_at=now()
                where status = %(from_status)s
                and updated_at < ( now() - (%(time_sec)s * interval '1 second'))
                ;
                """,
            {"from_status": (from_status,), "to_status": (to_status,), "time_sec": (time_sec,)},
        )

    # Update status of a batch item in the batch log, making sure to fail if the id and updated_at don't match, providing a guarantee of atomic operation
    # Returns updated_at, so caller can check if it was updated or not (compare it to argument)
    def bump_batch_item(self, id, status, error, updated_at, result=None):
        if result is None:
            return self.dbc.query_one(
                """
                    update batch_log
                        set status=%(status)s,
                        error = %(error)s,
                        updated_at=now()
                    where id = %(id)s
                    and updated_at = %(updated_at)s
                    returning id, updated_at
                    ;
                    """,
                {"id": (id,), "status": (status,), "error": (error,), "updated_at": (updated_at,)},
            )
        else:
            return self.dbc.query_one(
                """
                    update batch_log
                        set status=%(status)s,
                        error = %(error)s,
                        result = %(result)s,
                        updated_at=now()
                    where id = %(id)s
                    and updated_at = %(updated_at)s
                    returning id, updated_at
                    ;
                    """,
                {"id": (id,), "status": (status,), "error": (error,), "result": (result,), "updated_at": (updated_at,)},
            )

    # Simplified version of bump_batch_item where status is updated, no questions asked
    def bump_batch_item_status(self, id, status):
        self.dbc.query_none(
            """
                update batch_log
                    set status=%(status)s,
                    updated_at=now()
                where id = %(id)s
                ;
                """,
            {"id": (id,), "status": (status,)},
        )

    # Update a batch item in the batch log, making sure to fail if the id and updated_at don't match, providing a guarantee of atomic operation
    def book_batch_item(self, from_status=PENDING, to_status=IN_PROGRESS):
        return self.dbc.query_one(
            """
                update batch_log
                    set status=%(to_status)s,
                    updated_at=now()
                where status = %(from_status)s
                and id = (
                    select id
                    from batch_log
                    where true
                    and status = %(from_status)s
                    order by priority desc, updated_at asc
                    limit 1
                )
                returning id, priority, data, result, type, status, source, created_at, updated_at
                ;
                """,
            {"from_status": (from_status,), "to_status": (to_status,)},
        )

    # Update a batch item in the batch log, making sure to fail if the id and updated_at don't match, providing a guarantee of atomic operation
    # NOTE: This is the throttled version
    def book_throttled_batch_item(self, from_status=PENDING, to_status=IN_PROGRESS):
        return self.dbc.query_one(
            """
                update batch_log
                    set status=%(to_status)s,
                    updated_at=now()
                where status = %(from_status)s
                and id = (
                    select id
                    from batch_log
                    where true
                    and status = %(from_status)s
                    and gcra_throttle(throttle_key, throttle_limit, throttle_period, true)::int <=0
                    order by priority desc, updated_at asc
                    limit 1
                )
                returning id, priority, data, result, type, status, source, created_at, updated_at
                ;
                """,
            {"from_status": (from_status,), "to_status": (to_status,)},
        )

    # Delete batch items with given status and update_at longer than given time
    def delete_batch_items_with_status_older_than(self, status, updated_at):
        self.dbc.query_none(
            """
                delete from batch_log
                where status=%(status)s,
                and updated_at >= %(updated_at)s
                ;
                """,
            {"status": (status,), "updated_at": (updated_at,)},
        )

    # Clear out the batch items table
    def delete_all(self):
        return self.dbc.query_none(
            """
                delete from batch_log
                ;
                """
        )

    # Get batch items from batch log fitting the optional filter
    def get_batch_items(self, id=None, priority=None, type=None, status=None, throttle_key=None, source=None, limit=1):
        return self.dbc.query_many(
            """
                select
                    id,
                    priority,
                    data,
                    result,
                    type,
                    status,
                    throttle_key,
                    throttle_limit,
                    throttle_period,
                    source,
                    created_at,
                    updated_at
                from batch_log
                where true
                and (%(id)s is null or id = any(%(id)s))
                and (%(priority)s is null or priority = any(%(priority)s))
                and (%(type)s is null or type = any(%(type)s))
                and (%(status)s is null or status = any(%(status)s))
                and (%(throttle_key)s is null or throttle_key = any(%(throttle_key)s))
                and (%(source)s is null or source = any(%(source)s))
                order by priority desc, updated_at asc
                limit %(limit)s
                ;
                """,
            {"id": (id,), "priority": (priority,), "type": (type,), "status": (status,), "throttle_key": (throttle_key,), "source": (source,), "limit": (limit,)},
        )

    # Get batch item by id from batch log
    def get_batch_item_by_id(self, id):
        return self.dbc.query_one(
            """
                select
                    id,
                    priority,
                    data,
                    result,
                    type,
                    status,
                    throttle_key,
                    throttle_limit,
                    throttle_period,
                    source,
                    created_at,
                    updated_at
                from batch_log
                where id = %(id)s
                order by priority desc, updated_at asc
                limit 1
                ;
                """,
            {"id": (id,)},
        )

    # Get distinct batch types+status counts
    def get_type_status_counts(self):
        return self.dbc.query_many(
            """
                select
                    count(*) as count,
                    type as name,
                    status as status
                from batch_log
                group by type, status
                ;
                """
        )

    # Get distinct batch types with counts
    def get_type_counts(self):
        return self.dbc.query_many(
            """
                select
                    count(*) as count,
                    type as name
                from batch_log
                group by type
                ;
                """
        )

    # Get distinct batch status with counts
    def get_status_counts(self):
        return self.dbc.query_many(
            """
                select
                    count(*) as count,
                    status as name
                from batch_log
                group by status
                ;
                """
        )

    # Get count of ready pending batch items taking into acount throttling
    def get_throttled_pending_count(self):
        return self.dbc.query_many(
            """
                select
                    count(*) as count,
                    min(gcra_throttle(throttle_key, throttle_limit, throttle_period, false)) as wait_millis
                from batch_log
                ;
                """
        )

    # Get ready pending batch items taking into acount throttling
    def get_throttled_pending(self):
        return self.dbc.query_many(
            """
                select
                    id,
                    gcra_throttle(throttle_key, throttle_limit, throttle_period, false) as wait_millis
                from batch_log
                order by wait_millis asc
                ;
                """
        )

    def get_job_counts(self):
        return self.dbc.query_many(
            """
                select
                    type,
                    status,
                    count(*)
                from
                    batch_log
                group by
                    type,
                    status
                order by
                    type,
                    status
                ;
                """
        )

    # Get batch items from batch log sorted by last active
    def get_last_jobs(self, id=None, priority=None, type=None, status=None, throttle_key=None, source=None, error=None, limit=1):
        return self.dbc.query_many(
            """
                select
                    id,
                    priority,
                    data,
                    result,
                    type,
                    status,
                    throttle_key,
                    throttle_limit,
                    throttle_period,
                    error,
                    updated_at - created_at as runtime,
                    extract(EPOCH from (updated_at - created_at)) as runtime_ts,
                    updated_at,
                    created_at
                from batch_log
                where true
                and (%(id)s is null or id = any(%(id)s))
                and (%(priority)s is null or priority = any(%(priority)s))
                and (%(type)s is null or type = any(%(type)s))
                and (%(status)s is null or status = any(%(status)s))
                and (%(throttle_key)s is null or throttle_key = any(%(throttle_key)s))
                and (%(error)s is null or error = any(%(error)s))
                and (%(source)s is null or source = any(%(source)s))
                order by updated_at desc, runtime asc, priority desc
                limit %(limit)s
                ;
                """,
            {"id": (id,), "priority": (priority,), "type": (type,), "status": (status,), "throttle_key": (throttle_key,), "source": (source,), "error": (error,), "limit": (limit,)},
        )

    def get_now(self):
        r = self.dbc.query_one(
            """
                select now()
            ;"""
        )
        r = r.replace(tzinfo=pytz.UTC)
        return r

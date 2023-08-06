from omymodels import create_models


ddl = """CREATE table user_history (
     runid                 decimal(21) null
    ,job_id                decimal(21)  null
    ,id                    varchar(100) not null
    ,user              varchar(100) not null
    ,status                varchar(10) not null
    ,event_time            timestamp not null default NOW()
    ,comment           varchar(1000) default null
    ) ;"""

result = create_models(ddl, models_type="gino")
print(result)

-- filter out the film we want to rent out for free
with filtered_films as(
  select distinct film_id 
  from spiritual-hour-458020-c6.staging_db.stg_film
  where true
    and film_title != 'GOODFELLAS SALUTE'
)
,
-- get the inventory ids, where inventory id like the unique dvd we have for each film, that do not include this film
clean_inventory as (
  select distinct inventory_id
  from spiritual-hour-458020-c6.staging_db.stg_inventory inv
  inner join filtered_films ff
  on inv.film_id = ff.film_id
)
,
-- get the rental ids, like the id of each movie
clean_rental_ids as (
  select distinct rental_id
  from spiritual-hour-458020-c6.staging_db.stg_rental ren
  inner join clean_inventory ci
  on ren.inventory_id = ci.inventory_id
)
,
-- for our clean rental_ids get the necessary info from the payments table
payments as (
  select 
     coalesce(payment_amount,0) as payment_amount
    ,payment_date
  from spiritual-hour-458020-c6.staging_db.stg_payment p
  inner join clean_rental_ids cri
  on p.rental_id = cri.rental_id
)
,
-- choose relevant reporting dates (day, week, year) per project instructions
reporting_dates as(
  select *
  from spiritual-hour-458020-c6.reporting_db.reporting_periods_table
  where true
    and lower(reporting_period) in ('day','week','year')
    and reporting_date between date '2015-01-01' and current_date
)
,
--calculate the revenue per reporting date
-- we could use dynamic grouping here if more data is true
revenue_per_period as (
  select
    'Day' as reporting_period
    ,date(date_trunc(payments.payment_date,day)) as reporting_date
    ,sum(payment_amount) as total_revenue
    from payments
    group by 1,2
  union all
    select
    'Month' as reporting_period
    ,date(date_trunc(payments.payment_date,month)) as reporting_date
    ,sum(payment_amount) as total_revenue
    from payments
    group by 1,2
  union all
    select
    'Year' as reporting_period
    ,date(date_trunc(payments.payment_date,year)) as reporting_date
    ,sum(payment_amount) as total_revenue
    from payments
    group by 1,2
)
,
-- join the total revenue table with the reporting dates we have in the relevant table, per projects instr, if in the reporting data of our reporting table there is
-- no total revenue we should have zero values and not null values
final as (
  select 
     rd.reporting_date
    ,rd.reporting_period
    ,coalesce(total_revenue,0) as total_revenue
  from reporting_dates rd
  left join revenue_per_period rpp
  on rd.reporting_date = rpp.reporting_date
  and rd.reporting_period = rpp.reporting_period
)


select * 
from final
order by 1,2



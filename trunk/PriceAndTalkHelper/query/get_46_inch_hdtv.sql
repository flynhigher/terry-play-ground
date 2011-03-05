SELECT name, ifnull(part_number, model) model, ifnull(amazon_sales_rank,0) salesRank, amazon_review_rating rating, amazon_total_reviews total_review,
pp.price, pp.product_code, pp.source_url
FROM product_product p
inner join product_price pp on p.id = pp.product_id
where name like '%46-inch%' or name like '%46"%'
order by amazon_sales_rank  limit 1000
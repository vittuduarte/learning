SELECT seller_id, 
SUM(t1.price) AS totalRevenue,
COUNT(DISTINCT t1.order_id) AS qtSalles

FROM tb_orders_items AS t1
GROUP BY seller_id
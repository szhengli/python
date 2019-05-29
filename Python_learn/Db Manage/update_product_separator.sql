UPDATE %s
SET buy_product = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(buy_product,' ',''),'，',','),'）',')'),'（','('),'、',','),'\\',','),
sell_product = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(sell_product,' ',''),'，',','),'）',')'),'（','('),'、',','),'\\',',');
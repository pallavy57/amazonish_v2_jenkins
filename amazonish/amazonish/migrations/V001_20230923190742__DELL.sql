CREATE TABLE public.products (
    id character varying(255) NOT NULL,
    category_id character varying(255),
    title character varying(255),
    picture character varying(255),
    summary character varying(255),
    description character varying(255),
    price character varying(255),
    discount_type character varying(255),
    discount_value character varying(255),
    tags character varying(255),
    created_at date,
    updated_at date
);
ALTER TABLE public.products OWNER TO postgres;
 
CREATE TABLE public.categories (
    id character varying(255) NOT NULL,
    parent_category character varying(255),
    slug character varying(255),
    name character varying(255),
    description character varying(255),
    tags character varying(255),
    created_at date,
    updated_at date
);
ALTER TABLE public.categories OWNER TO postgres;
 
CREATE TABLE public.reviews (
    id character varying(255) NOT NULL,
    user_id character varying(255),
    product_id character varying(255),
    rating character varying(255),
    comment character varying(255),
    created_at date
);
ALTER TABLE public.reviews OWNER TO postgres;
 
CREATE TABLE public.users (
    id character varying(255) NOT NULL,
    slug character varying(255),
    email character varying(255),
    phone character varying(255),
    role character varying(255),
    name character varying(255),
    avatar character varying(255),
    locale character varying(255),
    created_at date,
    updated_at date,
    last_login character varying(255),
    email_validated character varying(255),
    phone_validated character varying(255),
    bio character varying(255),
    company character varying(255)
);
ALTER TABLE public.users OWNER TO postgres;
 
CREATE TABLE public.carts (
    id character varying(255) NOT NULL,
    created_by character varying(255),
    status character varying(255),
    created_at date,
    updated_at date
);
ALTER TABLE public.carts OWNER TO postgres;

CREATE TABLE public.cart_items (
    id character varying(255),
    cart_id character varying(255),
    product_id character varying(255),
    created_at date,
    price character varying(255),
    quantity character varying(255)
);
ALTER TABLE public.cart_items OWNER TO postgres;

CREATE TABLE public.orders (
    id character varying(255) NOT NULL,
    created_at date,
    user_id character varying(255)
);
ALTER TABLE public.orders OWNER TO postgres;


CREATE TABLE public.order_lines (
    id character varying(255) NOT NULL,
    order_id character varying(255),
    product_id character varying(255),
    price character varying(255),
    quantity character varying(255)
);
ALTER TABLE public.order_lines OWNER TO postgres;

 
ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 
ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);
 
ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_games_pkey PRIMARY KEY (id);
 
ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 
ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id); 

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.order_lines
    ADD CONSTRAINT order_lines_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.products
    ADD CONSTRAINT fk1kenmun90s7uhly5kkk9o6rsf FOREIGN KEY (category_id) REFERENCES public.categories(id);


-- ALTER TABLE ONLY public.users
--     ADD CONSTRAINT fk1kenmun90s7uhly5kkk9o6rsf FOREIGN KEY (product_id) REFERENCES public.products(id);
 
-- ALTER TABLE ONLY public.categories
--     ADD CONSTRAINT fk5ykqwib1neqhak6wwuhsusf5w FOREIGN KEY (category_id) REFERENCES public.categories(id);
 
ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fkfmhm06fi40ak53r6gofvoyr44 FOREIGN KEY (product_id) REFERENCES public.products(id);

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fkfmhm06fi40ak53r6gofuyu44 FOREIGN KEY (user_id) REFERENCES public.users(id);


ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fkhoasvgr0mq1tkj5308chmd97v FOREIGN KEY (user_id) REFERENCES public.users(id);
 
ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fkikaihvc8m29y7fqtk5brfwk48 FOREIGN KEY (product_id) REFERENCES public.products(id);
 
 ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT fkquj6n755j3k650vwhoabw44yu FOREIGN KEY (cart_id) REFERENCES public.carts(id);
 
ALTER TABLE ONLY public.order_lines
    ADD CONSTRAINT fkuqqdoorh4jhfx6mqe3wsy5ni FOREIGN KEY (order_id) REFERENCES public.orders(id);

ALTER TABLE ONLY public.order_lines
    ADD CONSTRAINT fkuqqdoorh4jhfx6mqe3wsy57i FOREIGN KEY (product_id) REFERENCES public.products(id);    

-- ALTER TABLE ONLY public.order_lines
--     ADD CONSTRAINT fkupqdoorh4jhfx6mqe3wsy5ny FOREIGN KEY (order_lines_id) REFERENCES public.order_lines(id);
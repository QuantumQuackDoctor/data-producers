create sequence if not exists hibernate_sequence;

alter sequence hibernate_sequence owner to rds_superuser;

create table if not exists user_entity_orders
(
    user_entity_id bigint not null,
    orders_id      bigint not null
        constraint uk_enkeibsmcd4blsut5v79brvpn
            unique
);

alter table user_entity_orders
   owner to rds_superuser;

create table if not exists configuration_entity
(
    id                 bigint not null
        constraint configuration_entity_pkey
            primary key,
    configuration_name varchar(255)
);

alter table configuration_entity
   owner to rds_superuser;

create table if not exists food_order_entity
(
    id            bigint not null
        constraint food_order_entity_pkey
            primary key,
    restaurant_id bigint
);

alter table food_order_entity
   owner to rds_superuser;

create table if not exists image_entity
(
    id    bigint not null
        constraint image_entity_pkey
            primary key,
    image oid
);

alter table image_entity
   owner to rds_superuser;

create table if not exists menu_item_entity
(
    id          bigint not null
        constraint menu_item_entity_pkey
            primary key,
    allergens   varchar(255),
    description varchar(255),
    image_id    varchar(255),
    name        varchar(255),
    price       real
);

alter table menu_item_entity
   owner to rds_superuser;

create table if not exists food_order_entity_order_items
(
    food_order_entity_id bigint not null
        constraint fkqbvmb0oyq0skc6ymgfpy47ln4
            references food_order_entity,
    order_items_id       bigint not null
        constraint fkmayeti61qg6evvqvu5tdrmvr0
            references menu_item_entity
);

alter table food_order_entity_order_items
   owner to rds_superuser;

create table if not exists menu_item_entity_configurations
(
    menu_item_entity_id bigint not null
        constraint fk13d71d7vdpyuq3jtx7d7q8ttt
            references menu_item_entity,
    configurations_id   bigint not null
        constraint uk_93h45rbhoy7tthbxlijii07ki
            unique
        constraint fk38jycf7x86u4u6s9ucruxhowf
            references configuration_entity
);

alter table menu_item_entity_configurations
   owner to rds_superuser;

create table if not exists order_configuration_entity
(
    id                 bigint not null
        constraint order_configuration_entity_pkey
            primary key,
    configuration_name varchar(255)
);

alter table order_configuration_entity
   owner to rds_superuser;

create table if not exists food_order_entity_configurations
(
    food_order_entity_id bigint not null
        constraint fkt3w5s8jv1mssros9krl1kt8g0
            references food_order_entity,
    configurations_id    bigint not null
        constraint uk_oaeb13wbtns1f6r51teby6h3f
            unique
        constraint fkelcgjrmg4nok8a15norc2arxn
            references order_configuration_entity
);

alter table food_order_entity_configurations
   owner to rds_superuser;

create table if not exists promotions_entity
(
    id        bigint not null
        constraint promotions_entity_pkey
            primary key,
    condition varchar(255),
    discount  varchar(255),
    name      varchar(255)
);

alter table promotions_entity
   owner to rds_superuser;

create table if not exists restaurant_entity
(
    id               bigint not null
        constraint restaurant_entity_pkey
            primary key,
    address          varchar(255),
    average_rating   integer,
    average_time     integer,
    background_id    varchar(255),
    geolocation      varchar(255),
    fri              varchar(255),
    mon              varchar(255),
    sat              varchar(255),
    sun              varchar(255),
    thu              varchar(255),
    tue              varchar(255),
    wed              varchar(255),
    icon_id          varchar(255),
    name             varchar(255),
    price_rating     integer,
    search_primary   varchar(255),
    search_secondary varchar(255)
);

alter table restaurant_entity
   owner to rds_superuser;

create table if not exists restaurant_entity_menu
(
    restaurant_entity_id bigint not null
        constraint fkaivijjx80dgs2mvlkf2f16klh
            references restaurant_entity,
    menu_id              bigint not null
        constraint uk_nwfmc2uv9inyk6a48htmqpxx1
            unique
        constraint fkaoctub7e0wrtmyevsffssc3qd
            references menu_item_entity
);

alter table restaurant_entity_menu
   owner to rds_superuser;

create table if not exists restaurant_entity_promotions
(
    restaurant_entity_id bigint not null
        constraint fks3h6ut0ne35d633s7hnbcleyw
            references restaurant_entity,
    promotions_id        bigint not null
        constraint uk_78iwoqtss1fb9huuba7t9utjn
            unique
        constraint fkjlpm36u5nfmo0itypyui7e7ob
            references promotions_entity
);

alter table restaurant_entity_promotions
   owner to rds_superuser;

create table if not exists user_role_entity
(
    id   bigint not null
        constraint user_role_entity_pkey
            primary key,
    role varchar(255)
        constraint uk_13eg2omx699idu6britk9wdc3
            unique
);

alter table user_role_entity
   owner to rds_superuser;

create table if not exists user_entity
(
    id                          bigint not null
        constraint user_entity_pkey
            primary key,
    activated                   boolean,
    activation_token            uuid,
    activation_token_expiration timestamp,
    birth_date                  date,
    email                       varchar(255)
        constraint uk_4xad1enskw4j1t2866f7sodrx
            unique,
    first_name                  varchar(255),
    is_veteran                  boolean,
    last_name                   varchar(255),
    password                    varchar(255),
    phone                       varchar(255),
    points                      integer,
    email_option                boolean,
    phone_option                boolean,
    dark                        boolean,
    user_role_id                bigint
        constraint fkovfl3qs88u908k064nsrxhq5a
            references user_role_entity
);

alter table user_entity
   owner to rds_superuser;

create table if not exists driver_entity
(
    car     varchar(255),
    user_id bigint not null
        constraint driver_entity_pkey
            primary key
        constraint fkp8yb3h7gd2x7muowrdx75w5uf
            references user_entity
);

alter table driver_entity
   owner to rds_superuser;

create table if not exists driver_rating_entity
(
    id          bigint not null
        constraint driver_rating_entity_pkey
            primary key,
    description varchar(255),
    stars       integer,
    user_id     bigint
        constraint fk9b6h56qq51m91036vn0ntq0ii
            references user_entity
);

alter table driver_rating_entity
   owner to rds_superuser;


create table if not exists driver_entity_ratings
(
    driver_entity_user_id bigint not null
        constraint fkfjypnd92y14lvfqknvjqvekwr
            references driver_entity,
    ratings_id            bigint not null
        constraint uk_3ys697ung1ahxxchpgql1xobj
            unique
        constraint fko78jqo7x1cxlfar94re7ve7tr
            references driver_rating_entity
);

alter table driver_entity_ratings
   owner to rds_superuser;

create table if not exists order_entity
(
    id                  bigint not null
        constraint order_entity_pkey
            primary key,
    active              boolean,
    address             varchar(255),
    delivery            boolean,
    driver_note         varchar(255),
    delivery_slot       timestamp,
    driver_accept       timestamp,
    driver_complete     timestamp,
    order_complete      timestamp,
    placed              timestamp,
    restaurant_accept   timestamp,
    restaurant_complete timestamp,
    restaurant_start    timestamp,
    delivery_price      real,
    food_price          real,
    tip                 real,
    refunded            boolean,
    restaurant_note     varchar(255),
    driver_user_id      bigint
        constraint fk5gg7hndjvs841icllb4njb2qt
            references driver_entity
            on delete set null,
    user_id             bigint
        constraint fk4na8ykxyemvs9auhondwoj7ir
            references user_entity
            on delete set null,
    confirmation_code   uuid
        constraint uk_4n2mrtpcfrl6kcnmer75xa2mk
            unique,
    payment_confirmed   boolean
);

alter table order_entity
   owner to rds_superuser;

create table if not exists order_entity_items
(
    order_entity_id bigint not null
        constraint fkro5obuq05ifhq64qlcjs36kmb
            references order_entity,
    items_id        bigint not null
        constraint uk_mprp1x0w14f8vshugkdjorrg4
            unique
        constraint fki0knhob3d4lj75xgrjrttc8ev
            references food_order_entity
);

alter table order_entity_items
   owner to rds_superuser;

create table if not exists restaurant_rating_entity
(
    id          bigint not null
        constraint restaurant_rating_entity_pkey
            primary key,
    description varchar(255),
    image_id    varchar(255),
    stars       integer,
    user_id     bigint
        constraint fkppaw9lio9x4e56odmhggtyn0k
            references user_entity
);

alter table restaurant_rating_entity
   owner to rds_superuser;

create table if not exists restaurant_entity_ratings
(
    restaurant_entity_id bigint not null
        constraint fkkb4nwtyvmyg6xrliayyc3pr3w
            references restaurant_entity,
    ratings_id           bigint not null
        constraint uk_bxpenr51d64j7e8nygkjqxxua
            unique
        constraint fki811ot03wo5kct6jfr75fmk1d
            references restaurant_rating_entity
);

alter table restaurant_entity_ratings
   owner to rds_superuser;

create table if not exists user_entity_order_list
(
    user_entity_id bigint not null
        constraint fkgvs19b7tw7tyaaw4arrq50sj5
            references user_entity,
    order_list_id  bigint not null
        constraint uk_4l1h1qogbja0pp9wbj2hle5mw
            unique
        constraint fk806lk1vp9b4y5hb39g7qhb51r
            references order_entity
);

alter table user_entity_order_list
   owner to rds_superuser;

SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
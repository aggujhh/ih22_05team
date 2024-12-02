#データベース作成
CREATE
    DATABASE ih22_db
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

# CREATE
-- USER 'ih05team'@'localhost' IDENTIFIED BY 'ih05_123456';
GRANT ALL PRIVILEGES ON ih22_db.* TO
    'ih05team'@'localhost';
FLUSH
    PRIVILEGES;

USE ih22_db;


#テーブル1
CREATE TABLE USERM
(
    user_id       char(10) primary key COMMENT 'ユーザーID',
    user_password varchar(255) not null COMMENT 'パスワード',
    user_type     char(1) DEFAULT '0' COMMENT 'ユーザー種類',
    user_status   char(1) DEFAULT '0' COMMENT 'ユーザー状態',
    create_time   datetime     not null COMMENT '作成時間',
    login_time    datetime COMMENT 'ログイン時間'
);
-- user_type: 0:依頼者, 1:制作者

INSERT INTO USERM (user_id, user_password, create_time)
VALUES ('U_00000001', '123456', NOW()),
       ('U_00000002', '123456', NOW()),
       ('U_00000003', '123456', NOW()),
       ('U_00000004', '123456', NOW()),
       ('U_00000005', '123456', NOW());


#テーブル2
CREATE TABLE USER_INFOM
(
    user_id             char(10) primary key,
    user_name_kanji     varchar(50),
    user_name_katakana  varchar(50),
    user_phone_number   char(11) unique,
    user_email_address  varchar(64) unique,
    user_account_number char(7) unique,
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);

INSERT INTO USER_INFOM (user_id, user_name_kanji, user_name_katakana, user_phone_number, user_email_address,
                        user_account_number)
VALUES ('U_00000001', '山田太郎', 'ヤマダタロウ', '08012345678', 'yamada.taro@example.com', '1234567'),
       ('U_00000002', '佐藤次郎', 'サトウジロウ', '08023456789', 'sato.jiro@example.com', '2345678'),
       ('U_00000003', '鈴木花子', 'スズキハナコ', '08034567890', 'suzuki.hanako@example.com', '3456789'),
       ('U_00000004', '田中一郎', 'タナカイチロウ', '08045678901', 'tanaka.ichiro@example.com', '4567890'),
       ('U_00000005', '松本春子', 'マツモトハルコ', '08056789012', 'matsumoto.haruko@example.com', '5678901');


#テーブル5
CREATE TABLE ACCOUNTM
(
    account_number      char(7) primary key COMMENT '口座番号',
    bank_code           char(4)     not null COMMENT '金融機関コード',
    branch_code         char(3)     not null COMMENT '支店コード',
    deposit_type        char(1)     not null COMMENT '預金種目',
    account_holder_name varchar(50) not null COMMENT '口座名義',
    FOREIGN KEY (account_number) REFERENCES USER_INFOM (user_account_number)
);

INSERT INTO ACCOUNTM (account_number, bank_code, branch_code, deposit_type, account_holder_name)
VALUES ('1234567', '0001', '101', '1', '山田太郎'),
       ('2345678', '0002', '102', '2', '佐藤次郎'),
       ('3456789', '0003', '103', '1', '鈴木花子'),
       ('4567890', '0004', '104', '2', '田中一郎'),
       ('5678901', '0005', '105', '1', '松本春子');


#テーブル4
CREATE TABLE DLB_ADTBL
(
    delivery_address_id  char(100) primary key,
    postal_code          char(7),
    prefecture           varchar(50) not null,
    city_town_village    varchar(50) not null,
    street_number        varchar(50) not null,
    building_room_number varchar(50) not null
);

INSERT INTO DLB_ADTBL (delivery_address_id, postal_code, prefecture, city_town_village, street_number,
                       building_room_number)
VALUES ('addr001', '1234567', '東京都', '渋谷区', '1-2-3', 'ハイツA 202号室'),
       ('addr002', '2345678', '大阪府', '北区', '4-5-6', 'グランドB 305号室'),
       ('addr003', '3456789', '神奈川県', '横浜市', '7-8-9', 'サンシャインC 101号室'),
       ('addr004', '4567890', '愛知県', '名古屋市', '10-11-12', 'パレスD 505号室'),
       ('addr005', '5678901', '北海道', '札幌市', '13-14-15', 'ツインタワーE 808号室');


#テーブル3
CREATE TABLE DLBTBL
(
    user_id             char(10),
    delivery_address_id char(100),
    PRIMARY KEY (user_id, delivery_address_id),
    FOREIGN KEY (user_id) REFERENCES USER_INFOM (user_id),
    FOREIGN KEY (delivery_address_id) REFERENCES DLB_ADTBL (delivery_address_id)
);

INSERT INTO DLBTBL (user_id, delivery_address_id)
VALUES ('U_00000001', 'addr001'),
       ('U_00000002', 'addr002'),
       ('U_00000003', 'addr003'),
       ('U_00000004', 'addr004'),
       ('U_00000005', 'addr005');

#テーブル6
CREATE TABLE BDYM
(
    user_id             char(10) primary key,
    neck_size           DECIMAL(4, 1),
    chest_width         DECIMAL(4, 1),
    bust                DECIMAL(4, 1),
    waist               DECIMAL(4, 1),
    hip                 DECIMAL(4, 1),
    thigh_circumference DECIMAL(4, 1),
    calf_circumference  DECIMAL(4, 1),
    ankle_circumference DECIMAL(4, 1),
    pants_length        DECIMAL(4, 1),
    total_length        DECIMAL(4, 1),
    shoulder_width      DECIMAL(4, 1),
    back_length         DECIMAL(4, 1),
    forearm_length      DECIMAL(4, 1),
    sleeve_length       DECIMAL(4, 1),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);

INSERT INTO BDYM (user_id, neck_size, chest_width, bust, waist, hip, thigh_circumference, calf_circumference,
                  ankle_circumference, pants_length, total_length, shoulder_width, back_length, forearm_length,
                  sleeve_length)
VALUES ('U_00000001', 38.5, 100.0, 95.0, 80.0, 90.0, 55.0, 35.0, 22.0, 100.0, 150.0, 45.0, 55.0, 50.0, 60.0),
       ('U_00000002', 39.0, 102.0, 97.0, 82.0, 92.0, 56.0, 36.0, 23.0, 101.0, 152.0, 46.0, 56.0, 51.0, 61.0),
       ('U_00000003', 37.0, 98.0, 93.0, 78.0, 88.0, 54.0, 34.0, 21.0, 99.0, 148.0, 44.0, 54.0, 49.0, 59.0),
       ('U_00000004', 38.0, 100.0, 95.0, 79.0, 89.0, 55.0, 35.0, 22.0, 100.0, 149.0, 45.0, 55.0, 50.0, 60.0),
       ('U_00000005', 36.5, 96.0, 91.0, 76.0, 85.0, 53.0, 33.0, 20.0, 98.0, 147.0, 43.0, 53.0, 48.0, 58.0);


#テーブル7
CREATE TABLE HEADM
(
    user_id            char(10) primary key,
    face_length        DECIMAL(4, 1),
    head_circumference DECIMAL(4, 1),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);
INSERT INTO HEADM (user_id, face_length, head_circumference)
VALUES ('U_00000001', 18.5, 55.0),
       ('U_00000002', 19.0, 56.5),
       ('U_00000003', 17.8, 54.0),
       ('U_00000004', 18.2, 55.8),
       ('U_00000005', 19.2, 57.0);

#テーブル8
CREATE TABLE HANDM
(
    user_id             char(10) primary key,
    hand_length         DECIMAL(4, 1),
    hand_width          DECIMAL(4, 1),
    wrist_circumference DECIMAL(4, 1),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);
INSERT INTO HANDM (user_id, hand_length, hand_width, wrist_circumference)
VALUES ('U_00000001', 18.5, 8.5, 16.0),
       ('U_00000002', 19.0, 9.0, 16.5),
       ('U_00000003', 17.8, 8.2, 15.8),
       ('U_00000004', 18.2, 8.7, 16.2),
       ('U_00000005', 19.2, 9.2, 16.8);

#テーブル9
CREATE TABLE FEETM
(
    user_id     char(10) primary key,
    foot_length DECIMAL(4, 1),
    foot_width  DECIMAL(4, 1),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);
INSERT INTO FEETM (user_id, foot_length, foot_width)
VALUES ('U_00000001', 26.5, 10.0),
       ('U_00000002', 27.0, 10.5),
       ('U_00000003', 25.8, 9.8),
       ('U_00000004', 26.2, 10.2),
       ('U_00000005', 27.5, 10.7);

#テーブル10
CREATE TABLE POINTM
(
    user_id          char(10) primary key,
    available_points int DEFAULT 0,
    pending_points   int DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);
INSERT INTO POINTM (user_id, available_points, pending_points)
VALUES ('U_00000001', 150, 30),
       ('U_00000002', 200, 50),
       ('U_00000003', 120, 20),
       ('U_00000004', 180, 40),
       ('U_00000005', 220, 60);

#テーブル12
CREATE TABLE CPON_INFOT
(
    coupon_id       varchar(10) primary key,
    coupon_title    varchar(20)  not null,
    discount_amount char(10)     not null,
    eligible_target varchar(200) not null,
    usage_condition varchar(200) not null,
    valid_period    date         not null
);
INSERT INTO CPON_INFOT (coupon_id, coupon_title, discount_amount, eligible_target, usage_condition, valid_period)
VALUES ('C001', '10%OFF', '10%', '全商品', '1回限り', '2024-12-31'),
       ('C002', '20%OFF', '20%', '衣装のみ', '2回利用可能', '2024-11-30'),
       ('C003', '500円OFF', '500円', '全商品', '3000円以上の購入時', '2024-10-31'),
       ('C004', '送料無料', '送料無料', '全商品', '5000円以上の購入時', '2024-09-30'),
       ('C005', '30%OFF', '30%', '造形のみ', '1回限り', '2024-08-31');

#テーブル11
CREATE TABLE CPONM
(
    user_id   char(10),
    coupon_id varchar(10),
    PRIMARY KEY (user_id, coupon_id),
    FOREIGN KEY (coupon_id) REFERENCES CPON_INFOT (coupon_id),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);
INSERT INTO CPONM (user_id, coupon_id)
VALUES ('U_00000001', 'C001'),
       ('U_00000002', 'C002'),
       ('U_00000003', 'C003'),
       ('U_00000004', 'C004'),
       ('U_00000005', 'C005');

-- テーブル14
CREATE TABLE REQUEST_DETAILS
(
    request_id       varchar(64) primary key,
    request_title    varchar(20)   not null,
    request_content  varchar(1000) not null,
    request_status   char(1)       not null,
    request_deadline date          not null
);
INSERT INTO REQUEST_DETAILS (request_id, request_title, request_content, request_status, request_deadline)
VALUES ('R_00000001', '衣装制作', 'アニメキャラクターの衣装をフルオーダーで制作', '0', '2024-12-31'),
       ('R_00000002', 'ウィッグカスタマイズ', 'キャラクターに合わせたウィッグのカスタマイズを依頼', '0', '2024-11-15'),
       ('R_00000003', '小道具作成', 'コスプレイベント用の武器や小道具を手作りで制作', '0', '2024-10-20'),
       ('R_00000004', '特殊メイク依頼', 'キャラクターの特徴を再現するための特殊メイクを依頼', '0', '2024-09-25'),
       ('R_00000005', '撮影依頼', 'コスプレ衣装を着てのプロフェッショナルな撮影依頼', '0', '2024-08-10');


#テーブル13
CREATE TABLE REQUEST
(
    user_id    char(10),
    request_id varchar(64),
    primary key (user_id, request_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST_DETAILS (request_id)
);
INSERT INTO REQUEST (user_id, request_id)
VALUES ('U_00000001', 'R_00000001'),
       ('U_00000002', 'R_00000002'),
       ('U_00000003', 'R_00000003'),
       ('U_00000004', 'R_00000004'),
       ('U_00000005', 'R_00000005');


#テーブル15
CREATE TABLE REQUEST_CATEGORY
(
    request_id  varchar(64),
    category_id char(5),
    primary key (request_id, category_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST_DETAILS (request_id)
);
INSERT INTO REQUEST_CATEGORY (request_id, category_id)
VALUES ('R_00000001', 'C001'),
       ('R_00000001', 'C002'),
       ('R_00000002', 'C003'),
       ('R_00000002', 'C004'),
       ('R_00000003', 'C005'),
       ('R_00000003', 'C006'),
       ('R_00000004', 'C003'),
       ('R_00000004', 'C004'),
       ('R_00000005', 'C005'),
       ('R_00000005', 'C006');

#テーブル16
CREATE TABLE REQUEST_IMG
(
    request_id varchar(64),
    photo_id   varchar(64),
    photo_url  varchar(200) not null unique,
    primary key (request_id, photo_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST_DETAILS (request_id)
);

INSERT INTO REQUEST_IMG (request_id, photo_id, photo_url)
VALUES ('R_00000001', 'P000000000000001', 'http://example.com/images/costume1.jpg'),
       ('R_00000002', 'P000000000000002', 'http://example.com/images/wig1.jpg'),
       ('R_00000003', 'P000000000000003', 'http://example.com/images/props1.jpg'),
       ('R_00000004', 'P000000000000004', 'http://example.com/images/makeup1.jpg'),
       ('R_00000005', 'P000000000000005', 'http://example.com/images/photo1.jpg');


#テーブル17
CREATE TABLE REQUEST_OTHER
(
    request_id         varchar(64) primary key,
    experience         char(1) not null,
    fabric_material    char(1) not null,
    reproducibility    char(1) not null,
    reference_material char(1) not null,
    reply_frequency    char(1) not null,
    request_budget     char(1) not null,
    required_points    TEXT,
    FOREIGN KEY (request_id) REFERENCES REQUEST_DETAILS (request_id)
);
INSERT INTO REQUEST_OTHER (request_id, experience, fabric_material, reproducibility, reference_material,
                           reply_frequency, request_budget, required_points)
VALUES ('R_00000001', '0', '0', '0', '0', '0', '0', '正確な寸法と生地サンプル'),
       ('R_00000002', 'B', 'A', 'B', 'B', 'A', 'B', '色の参考画像と生地指定'),
       ('R_00000003', 'A', 'C', 'A', 'A', 'C', 'A', '武器の設計図と素材リスト'),
       ('R_00000004', 'B', 'B', 'B', 'A', 'B', 'C', '特殊メイクの手順書'),
       ('R_00000005', 'A', 'A', 'A', 'C', 'A', 'B', '撮影用のポーズ集と参考資料');

#テーブル18
CREATE TABLE CREATOR
(
    user_id              char(10) primary key,
    request_availability char(1) DEFAULT '0',
    owned_tools          varchar(50),
    creator_notification varchar(1000),
    creator_level        char(1) DEFAULT '0'
);
INSERT INTO CREATOR (user_id, request_availability, owned_tools, creator_notification, creator_level)
VALUES ('U_00000001', '1', 'ミシン, ハサミ', '新しいオーダーを受け付け中です', '0'),
       ('U_00000002', '0', 'ウィッグセット, コスプレ用メイク道具', '現在は休業中です', '0'),
       ('U_00000003', '1', '縫製マシン, アイロン', '今月末までの依頼受付中', '0'),
       ('U_00000004', '1', '3Dプリンター, 塗装ツール', '小道具制作のみ受け付けています', '0'),
       ('U_00000005', '0', 'カメラ, 照明セット', '撮影関連の依頼のみ対応中', '0');

#テーブル19
CREATE TABLE PROFILE
(
    user_id              char(10) primary key,
    nickname             varchar(35) not null unique,
    gender               char(1) DEFAULT '0',
    profile              varchar(1000),
    hobby                varchar(200),
    icon_url             varchar(200),
    background_photo_url varchar(200)
);
INSERT INTO PROFILE (user_id, nickname, gender, profile, hobby, icon_url, background_photo_url)
VALUES ('U_00000001', 'CosTaro', '1', 'プロのコスプレ衣装制作経験10年。', 'コスプレ、縫製',
        'http://example.com/icon1.jpg', 'http://example.com/bg1.jpg'),
       ('U_00000002', 'WigMaster', '2', 'ウィッグカスタマイズのスペシャリスト。', 'ヘアスタイリング、コスプレ',
        'http://example.com/icon2.jpg', 'http://example.com/bg2.jpg'),
       ('U_00000003', 'CraftPro', '1', '小道具作りが得意なクラフトマンです。', '3Dプリント、塗装',
        'http://example.com/icon3.jpg', 'http://example.com/bg3.jpg'),
       ('U_00000004', 'MakeupArt', '2', '特殊メイクでキャラクターを完全に再現します。', 'メイク、映画鑑賞',
        'http://example.com/icon4.jpg', 'http://example.com/bg4.jpg'),
       ('U_00000005', 'PhotoAce', '1', 'プロフェッショナルな撮影技術を提供します。', '写真撮影、カメラ',
        'http://example.com/icon5.jpg', 'http://example.com/bg5.jpg');


#テーブル20
CREATE TABLE EXPERTISE
(
    user_id     char(10),
    category_id varchar(2),
    primary key (user_id, category_id),
    FOREIGN KEY (user_id) REFERENCES CREATOR (user_id)
);
INSERT INTO EXPERTISE (user_id, category_id)
VALUES ('U_00000001', '1'), -- CosTaro: 衣装制作
       ('U_00000002', '2'), -- WigMaster: ウィッグカスタマイズ
       ('U_00000003', '3'), -- CraftPro: 小道具制作
       ('U_00000004', '4'), -- MakeupArt: 特殊メイク
       ('U_00000005', '5');
-- PhotoAce: 撮影依頼


#テーブル21
CREATE TABLE RATING
(
    rated_user_id     char(10),
    evaluator_user_id char(10),
    delivery_deadline INT,
    quality           INT,
    price             INT,
    responsiveness    INT,
    overall_rating    INT,
    review            VARCHAR(1000),
    helpfulness       BOOLEAN,
    PRIMARY KEY (rated_user_id, evaluator_user_id),
    FOREIGN KEY (rated_user_id) REFERENCES USERM (user_id),
    FOREIGN KEY (evaluator_user_id) REFERENCES USERM (user_id)
);

INSERT INTO RATING (rated_user_id, evaluator_user_id, delivery_deadline, quality, price, responsiveness, overall_rating,
                    review, helpfulness)
VALUES ('U_00000001', 'U_00000002', 5, 4, 5, 4, 4, 'Great service, would recommend!', TRUE),
       ('U_00000002', 'U_00000003', 3, 3, 4, 3, 3, 'Satisfactory experience, but could improve.', FALSE),
       ('U_00000003', 'U_00000001', 7, 5, 5, 5, 5, 'Excellent quality and timely delivery!', TRUE),
       ('U_00000001', 'U_00000004', 2, 2, 3, 2, 2, 'Not satisfied with the service.', FALSE),
       ('U_00000004', 'U_00000003', 6, 4, 4, 4, 4, 'Good overall experience, will use again.', TRUE);


#テーブル22
CREATE TABLE DESIGN_PREVIEW
(
    user_id   char(10),
    image_id  INT,
    image_url VARCHAR(1000),
    PRIMARY KEY (user_id, image_id),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);

INSERT INTO DESIGN_PREVIEW (user_id, image_id, image_url)
VALUES ('U_00000001', 1, 'http://example.com/images/design1.jpg'),
       ('U_00000002', 2, 'http://example.com/images/design2.jpg'),
       ('U_00000003', 3, 'http://example.com/images/design3.jpg'),
       ('U_00000004', 4, 'http://example.com/images/design4.jpg'),
       ('U_00000005', 5, 'http://example.com/images/design5.jpg');


-- テーブル23
CREATE TABLE REQUEST_APPLY
(
    creator_id char(10),
    request_id varchar(64),
    PRIMARY KEY (creator_id, request_id),
    FOREIGN KEY (creator_id) REFERENCES USERM (user_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST (request_id)
);
-- REQUEST(request_id)はPRIMARY KEY or UNIQUE制約が設定されているか


INSERT INTO REQUEST_APPLY (creator_id, request_id)
VALUES ('U_00000001', 'R_00000001'),
       ('U_00000002', 'R_00000002'),
       ('U_00000003', 'R_00000003'),
       ('U_00000004', 'R_00000004'),
       ('U_00000005', 'R_00000005');


-- テーブル24
CREATE TABLE ORDER_MGR
(
    requester_id varchar(64),
    request_id   varchar(64),
    PRIMARY KEY (requester_id, request_id),
    FOREIGN KEY (requester_id) REFERENCES USERM (user_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST (request_id)
);

INSERT INTO ORDER_MGR (requester_id, request_id)
VALUES ('U_00000001', 'R_00000001'),
       ('U_00000002', 'R_00000002'),
       ('U_00000003', 'R_00000003'),
       ('U_00000004', 'R_00000004'),
       ('U_00000005', 'R_00000005');


#テーブル25
CREATE TABLE REQUEST_HISTORY
(
    requester_id       varchar(64),
    request_id         varchar(64),
    creator_id         char(10),
    contract_amount    INT,
    contract_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (requester_id, request_id, creator_id),
    FOREIGN KEY (requester_id) REFERENCES USERM (user_id),
    FOREIGN KEY (creator_id) REFERENCES USERM (user_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST (request_id)
);

INSERT INTO REQUEST_HISTORY (requester_id, request_id, creator_id, contract_amount)
VALUES ('U_00000001', 'R_00000001', 'U_00000002', 10000),
       ('U_00000002', 'R_00000002', 'U_00000003', 20000),
       ('U_00000003', 'R_00000003', 'U_00000004', 15000),
       ('U_00000004', 'R_00000004', 'U_00000001', 30000),
       ('U_00000005', 'R_00000005', 'U_00000002', 25000);


#テーブル26
CREATE TABLE ADMIN
(
    admin_id                 CHAR(10),
    admin_password           VARCHAR(255),
    password_expiration_date DATETIME,
    admin_permissions        char(7),
    PRIMARY KEY (admin_id)
);

INSERT INTO ADMIN (admin_id, admin_password, password_expiration_date, admin_permissions)
VALUES ('A_00000001', 'hashed_password_1', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0000001'),
       ('A_00000002', 'hashed_password_2', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0000010'),
       ('A_00000003', 'hashed_password_3', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0000100'),
       ('A_00000004', 'hashed_password_4', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0001000'),
       ('A_00000005', 'hashed_password_5', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0010000');


#テーブル14
CREATE TABLE admin_permissions
(
    permission_id   char(7),
    permission_name varchar(100) not null,
    PRIMARY KEY (permission_id)
);

INSERT INTO ADMIN_PERMISSIONS(permission_id, permission_name)
VALUES ('0000001', 'お知らせ'),
       ('0000010', 'お問い合わせ'),
       ('0000100', '制作者審査'),
       ('0001000', 'アクションログ'),
       ('0010000', 'アカウント関連'),
       ('0100000', '情報閲覧'),
       ('1000000', '管理者管理');


#テーブル27
CREATE TABLE INQUIRY
(
    inquiry_id       INT AUTO_INCREMENT,
    user_id          char(10),
    inquiry_name     VARCHAR(50),
    inquiry_mail     VARCHAR(64),
    inquiry_tel      VARCHAR(15),
    inquiry_category VARCHAR(100),
    inquiry_contents TEXT,
    inquiry_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    inquiry_status   TINYINT,
    PRIMARY KEY (inquiry_id),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);
INSERT INTO INQUIRY (user_id, inquiry_name, inquiry_mail, inquiry_tel, inquiry_category, inquiry_contents,
                     inquiry_status)
VALUES ('U_00000001', 'John Doe', 'john.doe@example.com', '123-456-7890', 'Service Inquiry',
        'I would like to know more about your services.', 0),
       ('U_00000002', 'Jane Smith', 'jane.smith@example.com', '234-567-8901', 'Technical Support',
        'I am having trouble logging into my account.', 1),
       ('U_00000003', 'Alice Brown', 'alice.brown@example.com', '345-678-9012', 'Billing Inquiry',
        'Can I get a refund for my recent purchase?', 0),
       ('U_00000004', 'Bob Johnson', 'bob.johnson@example.com', '456-789-0123', 'Feature Request',
        'I would like to suggest a new feature.', 0),
       ('U_00000005', 'Charlie Green', 'charlie.green@example.com', '567-890-1234', 'General Inquiry',
        'Do you have any promotional offers?', 1);


#テーブル28
CREATE TABLE PRODUCER_APP
(
    creator_application_id     char(12) primary key,
    creator_nickname_id        VARCHAR(12)  not null,
    creator_mail               VARCHAR(64)  not null unique,
    creator_password           VARCHAR(255) not null,
    creator_tel                VARCHAR(15)  not null,
    creator_history            TEXT         not null,
    creator_application_status char(1)      not null
);


#テーブル29
CREATE TABLE IMG_APP
(
    product_image_id       INT AUTO_INCREMENT,
    creator_application_id char(12),
    product_image_url      VARCHAR(255) not null unique,
    PRIMARY KEY (product_image_id),
    FOREIGN KEY (creator_application_id) REFERENCES PRODUCER_APP (creator_application_id)
);


#テーブル31
CREATE TABLE NOTIFICATION
(
    notification_id          INT AUTO_INCREMENT,
    notification_title       TEXT,
    notification_post_status char(1) not null,
    notification_post_time   DATETIME DEFAULT CURRENT_TIMESTAMP,
    notification_content     TEXT,
    PRIMARY KEY (notification_id)
);

INSERT INTO NOTIFICATION (notification_title, notification_post_status, notification_content)
VALUES ('System Maintenance', '1', 'The system will undergo maintenance on October 25.'),
       ('New Feature Released', '1', 'A new feature has been added to the dashboard.'),
       ('Security Alert', '1', 'Please update your password to enhance security.'),
       ('Weekly Newsletter', '0', 'Here is your weekly update of the top stories.'),
       ('Holiday Notice', '1', 'The office will be closed during the national holiday.');
# 0:下書き,1:投稿済み,2:削除

#テーブル30
CREATE TABLE NOTIFICATION_MGR
(
    notification_id         INT,
    user_id                 char(10),
    admin_id                char(10),
    notification_management char(1) not null,
    PRIMARY KEY (notification_id, user_id, admin_id),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id),
    FOREIGN KEY (notification_id) REFERENCES NOTIFICATION (notification_id),
    CHECK ((user_id IS NOT NULL AND admin_id IS NULL)
        OR (user_id IS NULL AND admin_id IS NOT NULL))
);

INSERT INTO NOTIFICATION_MGR (notification_id, user_id, admin_id, notification_management)
VALUES (1, 'U_00000001', NULL, '1'),
       (2, 'U_00000002', NULL, '0'),
       (3, 'U_00000001', NULL, '1'),
       (4, 'U_00000003', NULL, '0'),
       (5, 'U_00000002', NULL, '1');


#テーブル32
CREATE TABLE REPORT_FRAU
(
    fraud_report_id    INT AUTO_INCREMENT,
    reporter_user_id   char(10) not null,
    detection_type     char(1)  not null,
    violation_reason   TEXT,
    violation_judgment char(1)  not null,
    reported_user_id   char(10) not null,
    reported_time      DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (fraud_report_id),
    FOREIGN KEY (reporter_user_id) REFERENCES USERM (user_id),
    FOREIGN KEY (reported_user_id) REFERENCES USERM (user_id)
);

INSERT INTO REPORT_FRAU (reporter_user_id, detection_type, violation_reason, violation_judgment, reported_user_id)
VALUES ('U_00000001', '1', 'Inappropriate content', '1', 'U_00000002'),
       ('U_00000003', '2', 'Harassment in messages', '1', 'U_00000004'),
       ('U_00000005', '3', 'Spam advertising', '0', 'U_00000005'),
       ('U_00000002', '1', 'False information', '0', 'U_00000003'),
       ('U_00000004', '2', 'Threatening behavior', '0', 'U_00000005');


#テーブル38
CREATE TABLE CHAT
(
    chat_id int AUTO_INCREMENT,
    user_id char(10),
    PRIMARY KEY (chat_id, user_id),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);
INSERT INTO CHAT (user_id)
VALUES ('U_00000001'),
       ('U_00000002'),
       ('U_00000003'),
       ('U_00000004'),
       ('U_00000005');


#テーブル33
CREATE TABLE CHANNELS
(
    channel_id     INT AUTO_INCREMENT,
    chat_id        int,
    channel_status char(1) not null,
    PRIMARY KEY (channel_id, chat_id),
    FOREIGN KEY (chat_id) REFERENCES CHAT (chat_id)
);
INSERT INTO CHANNELS (chat_id, channel_status)
VALUES (1, '1'), -- チャットID 1に対するチャネル
       (1, '0'), -- チャットID 1に別のチャネル
       (2, '1'), -- チャットID 2に対するチャネル
       (3, '1'), -- チャットID 3に対するチャネル
       (4, '0');
-- チャットID 4に対するチャネル


#テーブル34
CREATE TABLE MESSAGE
(
    message_id        BIGINT UNSIGNED AUTO_INCREMENT,
    chat_id           INT,
    channel_id        INT,
    message_content   TEXT,
    message_sent_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (message_id, channel_id),
    FOREIGN KEY (chat_id, channel_id) REFERENCES CHANNELS (chat_id, channel_id)
);
INSERT INTO MESSAGE (chat_id, channel_id, message_content)
VALUES (1, 1, 'Hello, how are you?'),
       (1, 1, 'What time is the meeting?'),
       (1, 2, 'Can anyone share the document?'),
       (2, 3, 'Looking forward to our project.'),
       (3, 4, 'Please confirm your attendance.');


#テーブル35
CREATE TABLE THAW_REQ
(
    unfreeze_request_id     INT AUTO_INCREMENT,
    user_id                 char(10),
    unfreeze_request_email  VARCHAR(64) not null,
    unfreeze_request_reason TEXT,
    unfreeze_request_status char(1)     not null,
    PRIMARY KEY (unfreeze_request_id),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);

INSERT INTO THAW_REQ (user_id, unfreeze_request_email, unfreeze_request_reason, unfreeze_request_status)
VALUES ('U_00000001', 'user1@example.com', 'I would like to reactivate my account.', 0),
       ('U_00000002', 'user2@example.com', 'Mistakenly froze my account.', 1),
       ('U_00000003', 'user3@example.com', 'Account was frozen due to inactivity.', 0),
       ('U_00000004', 'user4@example.com', 'Need access to my account urgently.', 2),
       ('U_00000005', 'user5@example.com', 'I have resolved the issues that led to freezing.', 1);


#テーブル36
CREATE TABLE FROZEN_USER
(
    user_id       char(10),
    freeze_reason TEXT,
    freeze_time   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);

INSERT INTO FROZEN_USER (user_id, freeze_reason)
VALUES ('U_00000001', 'Account frozen due to multiple failed login attempts.'),
       ('U_00000002', 'User requested account freeze for security reasons.'),
       ('U_00000003', 'Account inactive for over 6 months.'),
       ('U_00000004', 'Fraudulent activity detected on the account.'),
       ('U_00000005', 'User reported lost access and requested freeze.');


#テーブル37
CREATE TABLE DEL_USER
(
    user_id         char(10),
    deletion_reason TEXT,
    deletion_time   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);

INSERT INTO DEL_USER (user_id, deletion_reason)
VALUES ('U_00000001', 'User requested account deletion.'),
       ('U_00000002', 'User inactive for over 1 year.'),
       ('U_00000003', 'Account compromised, user requested deletion.'),
       ('U_00000004', 'User switched to a competitors service.'),
       ('U_00000005', 'User reported issues and chose to delete account.');


-- テーブル39
CREATE TABLE DEALCONFIRMATION
(
    contract_id      INT AUTO_INCREMENT,
    request_id       varchar(64) not null,
    creator_id       char(10)    not null,
    payment_amount   INT,
    contract_details TEXT,
    contract_stage   char(1)     not null,
    PRIMARY KEY (contract_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST (request_id),
    FOREIGN KEY (creator_id) REFERENCES USERM (user_id)
);

INSERT INTO DEALCONFIRMATION (contract_id, request_id, creator_id, payment_amount, contract_details, contract_stage)
VALUES (1, 'R_00000001', 'U_00000001', 5000, 'Contract for web development services.', '0'),
       (2, 'R_00000002', 'U_00000002', 3000, 'Design contract for marketing materials.', '1'),
       (3, 'R_00000003', 'U_00000003', 7500, 'Consultation services contract.', '2'),
       (4, 'R_00000004', 'U_00000004', 15000, 'Software development agreement.', '1'),
       (5, 'R_00000005', 'U_00000005', 2000, 'SEO services contract.', '2');


#テーブル40
CREATE TABLE TRANSACTION_MGR
(
    contract_id     INT,
    payment_date    DATE,
    transfer_date   DATE,
    transfer_status char(1) not null,
    PRIMARY KEY (contract_id),
    FOREIGN KEY (contract_id) REFERENCES DEALCONFIRMATION (contract_id)
);

INSERT INTO TRANSACTION_MGR (contract_id, payment_date, transfer_date, transfer_status)
VALUES (1, '2024-10-01', '2024-10-02', '1'),
       (2, '2024-10-03', '2024-10-04', '1'),
       (3, '2024-10-05', NULL, '0'),
       (4, '2024-10-06', NULL, '0'),
       (5, '2024-10-07', '2024-10-08', '1');


-- ==================================================================
-- database触った、2024.11.07
-- ==================================================================
drop table ORDER_MGR;
drop table REQUEST_APPLY;
drop table REQUEST_OTHER;
drop table REQUEST_IMG;
drop table REQUEST_CATEGORY;
drop table REQUEST_HISTORY;
drop table TRANSACTION_MGR;
drop table DEALCONFIRMATION;
drop table REQUEST;
drop table REQUEST_DETAILS;



CREATE TABLE REQUEST_DETAILS
(
    request_id       varchar(64) primary key,
    request_title    varchar(40),
    request_content  varchar(1000),
    request_status   char(1),
    request_deadline date
);

CREATE TABLE REQUEST
(
    user_id    char(10),
    request_id varchar(64),
    primary key (user_id, request_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST_DETAILS (request_id)
);

CREATE TABLE REQUEST_CATEGORY
(
    request_id    varchar(64),
    category_name varchar(20),
    primary key (request_id, category_name),
    FOREIGN KEY (request_id) REFERENCES REQUEST_DETAILS (request_id)
);
--
CREATE TABLE REQUEST_IMG
(
    request_id varchar(64),
    photo_name varchar(255),
    primary key (request_id, photo_name),
    FOREIGN KEY (request_id) REFERENCES REQUEST_DETAILS (request_id)
);
--
CREATE TABLE REQUEST_OTHER
(
    request_id         varchar(64) primary key,
    experience         char(1) not null,
    fabric_material    char(1) not null,
    reproducibility    char(1) not null,
    reference_material char(1) not null,
    reply_frequency    char(1) not null,
    request_budget     char(1) not null,
    required_points    TEXT,
    required_amount    INT,
    FOREIGN KEY (request_id) REFERENCES REQUEST_DETAILS (request_id)
);

CREATE TABLE REQUEST_APPLY
(
    creator_id char(10),
    request_id varchar(64),
    PRIMARY KEY (creator_id, request_id),
    FOREIGN KEY (creator_id) REFERENCES USERM (user_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST (request_id)
);

CREATE TABLE ORDER_MGR
(
    requester_id varchar(64),
    request_id   varchar(64),
    PRIMARY KEY (requester_id, request_id),
    FOREIGN KEY (requester_id) REFERENCES USERM (user_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST (request_id)
);

CREATE TABLE REQUEST_HISTORY
(
    requester_id       varchar(64),
    request_id         varchar(64),
    creator_id         char(10),
    contract_amount    INT,
    contract_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (requester_id, request_id, creator_id),
    FOREIGN KEY (requester_id) REFERENCES USERM (user_id),
    FOREIGN KEY (creator_id) REFERENCES USERM (user_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST (request_id)
);

CREATE TABLE DEALCONFIRMATION
(
    contract_id      INT AUTO_INCREMENT,
    request_id       varchar(64) not null,
    creator_id       char(10)    not null,
    payment_amount   INT,
    contract_details TEXT,
    contract_stage   char(1)     not null,
    PRIMARY KEY (contract_id),
    FOREIGN KEY (request_id) REFERENCES REQUEST (request_id),
    FOREIGN KEY (creator_id) REFERENCES USERM (user_id)
);

CREATE TABLE TRANSACTION_MGR
(
    contract_id     INT,
    payment_date    DATE,
    transfer_date   DATE,
    transfer_status char(1) not null,
    PRIMARY KEY (contract_id),
    FOREIGN KEY (contract_id) REFERENCES DEALCONFIRMATION (contract_id)
);



-- ===================================================
-- database 変更 2024/11/11
-- ===================================================
drop table admin;
drop table admin_permissions;

CREATE TABLE ADMIN
(
    admin_id                 CHAR(10),
    admin_name               VARCHAR(64),
    admin_password           VARCHAR(255),
    password_expiration_date DATETIME,
    admin_permissions        char(7),
    PRIMARY KEY (admin_id)
);

INSERT INTO ADMIN (admin_id, admin_name, admin_password, password_expiration_date, admin_permissions)
VALUES ('A_00000001', 'ロイド・フォージャー', 'hashed_password_1', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0000001'),
       ('A_00000002', 'ヨル・フォージャー', 'hashed_password_2', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0000010'),
       ('A_00000003', 'アーニャ・フォージャー', 'hashed_password_3', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0000100'),
       ('A_00000004', 'ボンド・フォージャー', 'hashed_password_4', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0001000'),
       ('A_00000005', 'ユーリ・ブライアー', 'hashed_password_5', DATE_ADD(NOW(), INTERVAL 1 MONTH), '0010000');


CREATE TABLE admin_permissions
(
    permission_id   char(7),
    permission_name varchar(100) not null,
    PRIMARY KEY (permission_id)
);

INSERT INTO ADMIN_PERMISSIONS(permission_id, permission_name)
VALUES ('0000001', 'お知らせ'),
       ('0000010', 'お問い合わせ'),
       ('0000100', '制作者審査'),
       ('0001000', 'アクションログ'),
       ('0010000', 'アカウント関連'),
       ('0100000', '情報閲覧'),
       ('1000000', '管理者管理');

-- ===================================================
-- database 変更 2024/11/12 陳昱光
-- ===================================================
-- 電話番号の項目削除
ALTER TABLE inquiry
    DROP inquiry_tel;


-- ===================================================
-- database 変更 2024/11/14 宮本康弘
-- ===================================================
-- DESIGN_PREVIEWの変更
DROP TABLE DESIGN_PREVIEW;
CREATE TABLE DESIGN_PREVIEW
(
    user_id   char(10),
    image_id  INT AUTO_INCREMENT,
    image_url VARCHAR(1000),
    PRIMARY KEY (image_id), -- image_idを単独の主キーにする
    FOREIGN KEY (user_id) REFERENCES USERM (user_id)
);

INSERT INTO DESIGN_PREVIEW (user_id, image_url)
VALUES ('U_00000001', 'http://example.com/images/design1.jpg'),
       ('U_00000002', 'http://example.com/images/design2.jpg'),
       ('U_00000003', 'http://example.com/images/design3.jpg'),
       ('U_00000004', 'http://example.com/images/design4.jpg'),
       ('U_00000005', 'http://example.com/images/design5.jpg');


-- ===================================================
-- database 変更 2024/11/18 陳昱光
-- ===================================================
-- EXPERTISEの変更
ALTER TABLE expertise DROP FOREIGN KEY expertise_ibfk_1;
ALTER TABLE expertise DROP PRIMARY KEY;
ALTER TABLE expertise
    DROP category_id;
ALTER TABLE expertise
    ADD category_name char(60);
ALTER TABLE expertise CHANGE COLUMN category_name categorys CHAR(60);

-- design_previewの変更
--外部キー制約削除
ALTER TABLE design_preview DROP FOREIGN KEY design_preview_ibfk_1;
--プライマリーキー削除
ALTER TABLE design_preview DROP PRIMARY KEY;
-- ALTER TABLE design_preview
--     DROP image_id;
ALTER TABLE design_preview
    change image_url images TEXT;




-- ===================================================
-- database 変更 2024/11/25 宮本康弘
-- ===================================================
CREATE TABLE LOG
(
    id   INT AUTO_INCREMENT,
    admin_id CHAR(10),
    action   CHAR(255),
    details  TEXT,
    time     DATETIME DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (id),
    FOREIGN KEY(admin_id) REFERENCES ADMIN (admin_id)
);

--- ==================================================
--- database 変更 宮本康弘
--- ==================================================
ALTER TABLE ADMIN
ADD COLUMN status CHAR(1) DEFAULT '1' NOT NULL;
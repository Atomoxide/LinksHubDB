insert into subcategory (subcategory_name, category_id) values
('gear_build', 3),
('loot_schedule', 3),
('info', 2),
('official', 2),
('plugin', 2);

insert into item (item_name, item_description, item_url, category_id, subcategory_id) values
('中量级时间轴', 'M5S~M8S时间轴，奶轴文档', 'https://docs.qq.com/sheet/DUWhySkpEVmt5Y1Zh?tab48z5mh=&tab=48z5mh', 5, 8),
('WTFDIG', '国际服所有常见攻略打法的图文和站位汇总', 'https://wtfdig.info/', 1, 2),
('MMW M5S','【MMW攻略组&苏帕酱噗】M5S 阿卡狄亚零式登天斗技场 中量级1 攻略详解','https://www.bilibili.com/video/BV1pNNyzxEh6/', 5, 8),
('MMW M6S','【MMW攻略组&苏帕酱噗】M6S 阿卡狄亚零式登天斗技场 中量级2 攻略详解','https://www.bilibili.com/video/BV1riKdzoESQ/', 5, 8),
('MMW M7S','【MMW攻略组&苏帕酱噗】M7S 阿卡狄亚零式登天斗技场 中量级3 攻略详解','https://www.bilibili.com/video/BV1293AzAESs/', 5, 8),
('MMW M8S门神','【MMW攻略组&苏帕酱噗】M8S 阿卡狄亚零式登天斗技场 中量级4 前半 攻略详解','https://www.bilibili.com/video/BV1aT3tzrEnq/', 5, 8),
('MMW M8S本体', '【MMW攻略组&苏帕酱噗】M8S 阿卡狄亚零式登天斗技场 中量级4 后半 攻略详解', 'https://www.bilibili.com/video/BV1gj3uzXEuB/', 5, 8),
('中文Wiki','FF14中文维基','https://ff14.huijiwiki.com/wiki/', 2, 5),
('国服狩猎时间表','国服各大区各服务器的A怪狩猎时间表一览，一只10点天道神典石！','https://www.kdocs.cn/l/csd1ymWeo1HY', 2, 5),
('绝杀宗长','幻巧宗长拼图棋盘枚举','https://docs.qq.com/sheet/DS3dSWnlEdWZxWFls?tab=BB08J3', 2, 5),
('网页跨大区','超域传送','https://ff14bjz.sdo.com/RegionKanTelepo', 2, 6),
('XIVALEXANDER','亚历山大，高ping双插插件','https://github.com/Soreepeong/XivAlexander', 2, 7);

insert into meta (meta_name, meta_content) values
('announcement', '暂无'),
('channels', 'about:blank');

update subcategory set subcategory_description = '视频版攻略链接' where subcategory_id = 1;
update subcategory set subcategory_description = '图文版攻略链接' where subcategory_id = 2;
update subcategory set subcategory_description = '配装信息汇总' where subcategory_id = 3;
update subcategory set subcategory_description = '掉落装备分配表' where subcategory_id = 4;
update subcategory set subcategory_description = '各类资料汇总' where subcategory_id = 5;
update subcategory set subcategory_description = '官方相关链接' where subcategory_id = 6;
update subcategory set subcategory_description = '第三方插件' where subcategory_id = 7;
update subcategory set subcategory_description = '7.2版本链接归档' where subcategory_id = 8;

insert into item (item_name, item_description, item_url, category_id, subcategory_id) values
('全职业开荒毕业配装','全职业开荒、禁断、毕业装备BIS表格','https://docs.qq.com/sheet/DUWhySkpEVmt5Y1Zh?tab48z5mh=&tab=48z5mh', 3, 3),
('掉落装备分配表','固定队的装备分配表','https://docs.qq.com/sheet/DUWhySkpEVmt5Y1Zh?tab=48z5mh=&tab=48z5mh', 3, 4);

insert into local (label, zh) values
('guide', '攻略'),
('video_guide', '视频攻略'),
('web_guide', '网页攻略'),
('gear', '装备'),
('gear_build', '配装'),
('loot_schedule', '分配表格'),
('hunt', '怪物狩猎'),
('hunt_schedule', 'A怪狩猎时间表'),
('tool', '外部工具'),
('info', '资讯'),
('official', '官方'),
('plugin', '插件'),
('archive', '旧版本归档');

update meta set meta_content = '暂无公告\nQQ群：1039708188' where meta_name = 'announcement';
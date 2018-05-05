#! -*- coding: utf-8 -*-
from DbConnection import DbConnection


class DbInteraction:
    """Класс выполнения запросов в БД"""
    def get_appeals(self):
        """Получение списка обращений"""
        statement = """SELECT *
                         FROM Appeals"""
        return DbConnection().execute_sql_statement(statement)

    def get_actions(self):
        """Получение списка действий из ЛК"""
        statement = """SELECT * 
                         FROM Actions"""
        return DbConnection().execute_sql_statement(statement)

    def get_appeal_themes(self):
        """Получение списка тем обращений"""
        statement = """SELECT *
                         FROM Appeal_themes"""
        return DbConnection().execute_sql_statement(statement)

    def get_channels(self):
        """Получение списка каналов"""
        statement = """SELECT *
                         FROM Channels"""
        return DbConnection().execute_sql_statement(statement)

    def get_rate_plans(self):
        """Получение списка тарифных планов"""
        statement = """SELECT *
                         FROM Rate_Plans"""
        return DbConnection().execute_sql_statement(statement)

    def get_appeals_actions_union(self, subs_id=None):
        """Получение данных из обращений и действий"""
        if subs_id:
            statement = """select un.* 
                              from (select apl.subs_id, aplt.def as theme, rtpl.def, apl.reg_date as Datetime, ch.def
                                      from Appeals apl
                                      join Appeal_themes aplt on apl.theme_id = aplt.theme_id
                                      join Channels ch        on apl.channel_id = ch.channel_id
                                      join Rate_Plans rtpl    on apl.rate_plan_id = rtpl.rate_plan_id
                            
                                   union
                              
                                  select act.subs_id, lk_act.name_actions as theme, rtpl.def, act.action_date as Datetime, ch.def
                                    from Actions act
                                    join Channels ch        on act.channel_id = ch.channel_id
                                    join Rate_Plans rtpl    on act.rate_plan_id = rtpl.rate_plan_id
                                    join lk_actions lk_act  on act.lk_actions_id = lk_act.lk_actions_id) as un
                             where un.subs_id in ({})
                             order by un.subs_id asc,
                                      un.Datetime asc""".format(subs_id)
        else:
            statement = """select un.* 
                              from (select apl.subs_id, aplt.def as theme, rtpl.def, apl.reg_date as Datetime, ch.def
                                      from Appeals apl
                                      join Appeal_themes aplt on apl.theme_id = aplt.theme_id
                                      join Channels ch        on apl.channel_id = ch.channel_id
                                      join Rate_Plans rtpl    on apl.rate_plan_id = rtpl.rate_plan_id
    
                                   union
    
                                  select act.subs_id, lk_act.name_actions as theme, rtpl.def, act.action_date as Datetime, ch.def
                                    from Actions act
                                    join Channels ch        on act.channel_id = ch.channel_id
                                    join Rate_Plans rtpl    on act.rate_plan_id = rtpl.rate_plan_id
                                    join lk_actions lk_act  on act.lk_actions_id = lk_act.lk_actions_id) as un
                             order by un.subs_id asc,
                                      un.Datetime asc"""

        return DbConnection().execute_sql_statement(statement)


if __name__ == "__main__":
    print(DbInteraction().get_appeals())
    print(DbInteraction().get_actions())
    print(DbInteraction().get_appeal_themes())
    print(DbInteraction().get_channels())
    print(DbInteraction().get_rate_plans())
    print(DbInteraction().get_appeals_actions_union())

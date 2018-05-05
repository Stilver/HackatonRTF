#! -*- coding: utf-8 -*-
from DbInteraction import DbInteraction
from datetime import datetime, timedelta


appeal_types = ["Единичное", "Родительское", "Повторно-родительское", "Повторное"]


class Magic:
    """Класс с основной логикой построения цепочек"""

    def get_and_sort_selected_items(self, subs_id=None):
        """Преобразуем записи из БД в более удобный формат, группируя потенциальные узлы цепочки в один список"""
        statement_result = DbInteraction().get_appeals_actions_union(subs_id)
        result = []
        ind = 0
        for index, tup in enumerate(statement_result):
            if ind:
                if tup[0] == accumlator[ind - 1][0] \
                   and tup[3] >= accumlator[ind - 1][3] \
                   and tup[3] <= accumlator[ind - 1][3] + timedelta(days=1):
                    accumlator.append(list(tup))
                    ind += 1
                else:
                    result.append(accumlator.copy())
                    accumlator = [list(tup)]
                    ind = 1
            else:
                accumlator = [list(tup)]
                ind += 1

            if index + 1 == len(statement_result):
                result.append(accumlator.copy())
        return result

    def reformat_chains(self, subs_id=None):
        """Преобразуем цепочки в удобный для предоставления вид"""
        raw_chains = self.get_and_sort_selected_items(subs_id)
        result = []

        for chain in raw_chains:
            # Выделяем идентификатор абонента и название ТП в отдельный элемент цепочки
            pure_chain = [[chain[0][0], chain[0][2]]]

            # Проставляем признак каждому узлу цепочки
            if len(chain) == 1:
                chain[0].append(appeal_types[0])
            else:
                chain[0].append(appeal_types[1])
                chain[-1].append(appeal_types[3])
                for i in range(len(chain) - 2):
                    chain[i + 1].append(appeal_types[2])

            # Формируем узлы цепочки действий абонента
            for node in chain:
                pure_chain.append([node[1], node[3], node[4], node[5]])

            result.append(pure_chain)

        return result


if __name__ == "__main__":
    Magic().reformat_chains()

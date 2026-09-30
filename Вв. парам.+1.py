# -*- coding: utf-8 -*-
from pyrevit import revit, forms
import Autodesk.Revit.DB as DB

doc = revit.doc

param_name = "ADSK_Примечание"

def update_selected_elements():
    # Используем глобальную переменную для запоминания предыдущего значения
    global base_value
    if 'base_value' not in globals():
        base_value = "Ст.К1-"  # Значение по умолчанию при первом запуске

    # Запрашиваем у пользователя базовое значение
    base_value = forms.ask_for_string(
        prompt="Введите значение для параметра:",
        default=base_value,
        title="Значение параметра"
    )
    
    if not base_value:
        forms.alert("Вы не ввели значение. Скрипт завершен.", title="Внимание")
        return

    selection = revit.get_selection()
    
    if not selection:
        forms.alert("Вы ничего не выделили. Скрипт завершен.", title="Внимание")
        return  # Завершаем выполнение скрипта, если ничего не выделено

    count = 0
    errors = []
    
    with revit.Transaction("Update Parameter: " + param_name):
        for el in selection:
            try:
                param = el.LookupParameter(param_name)
                
                if not param:
                    errors.append("Элемент ID {}: Параметр '{}' не найден".format(el.Id, param_name))
                    continue
                
                if param.IsReadOnly:
                    errors.append("Элемент ID {}: Параметр только для чтения".format(el.Id))
                    continue

                # Определяем тип параметра и текущее значение
                p_type = param.StorageType
                current_val = ""
                
                if p_type == DB.StorageType.String:
                    current_val = param.AsString() or ""
                elif p_type == DB.StorageType.Double:
                    current_val = str(param.AsDouble())
                elif p_type == DB.StorageType.Integer:
                    current_val = str(param.AsInteger())
                elif p_type == DB.StorageType.ElementId:
                    current_val = str(param.AsElementId())

                # Обновляем параметр на конкретное значение
                new_value = base_value
                if current_val != new_value:
                    if p_type == DB.StorageType.String:
                        param.Set(new_value)
                        count += 1
                    else:
                        errors.append("Элемент ID {}: Тип параметра не String (это {})".format(el.Id, p_type))
                else:
                    # Значение уже совпадает
                    pass

            except Exception as e:
                errors.append("Элемент ID {}: Ошибка: {}".format(el.Id, str(e)))
        
        # Итоговый отчет
        if count > 0:
            forms.alert("Успешно обновлено элементов: {}".format(count), title="Результат")
        
        if errors:
            error_msg = "\n".join(errors)
            forms.alert(error_msg, title="Ошибки выполнения")

if __name__ == "__main__":
    update_selected_elements()
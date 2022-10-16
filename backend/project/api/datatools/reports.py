import csv
from django.db.models import QuerySet
from django.http import HttpResponse


class ReportCsv:
    def __init__(self, qs: QuerySet, columns, user) -> None:
        super().__init__()
        self.qs = qs
        self.fields = columns
        self.user = user

    def delete_duplicate(self, output: list) -> list:
        """Нахождение и удаление дублирующихся ингредиентов"""
        removed_index = []
        for i in range(len(output)):
            for j in range(len(output) - i - 1):
                if output[i][0] == output[i + j + 1][0]:
                    output[i][1] += output[i + j + 1][1]
                    removed_index.append(output[i + j + 1])

        for i in removed_index:
            # try/except в случаях когда нужно удалить
            # более одного совпадающего по весу ингридиента
            try:
                output.remove(i)
            except ValueError:
                continue
        return output

    def get_http_response(self) -> HttpResponse:
        """Создание и отдача .csv отчета."""
        output = []
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Shopping cart - {self.user}.csv"'
        writer = csv.writer(response)
        writer.writerow(self.fields)
        for obj in self.qs:
            for ingredient_amount in obj.recipe.ingredientamounts.all():
                output.append(
                [
                    ingredient_amount.ingredient.name,
                    ingredient_amount.amount,
                    ingredient_amount.ingredient.measurement_unit
                ]
                )

        output = self.delete_duplicate(output)
        writer.writerows(output)
        return response

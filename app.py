import flet as ft

from logics_book import (
    add_book,
    get_books,
    update_book,
    delete_book,
)


def main(page: ft.Page):
    currency = "сом"
    page.title = "Библиотека"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F4F1EA"
    page.padding = 0
    page.window.width = 800
    page.window.height = 800
    page.window.min_width = 800
    page.window.min_height = 800

    title_field = ft.TextField(
        label="Название книги",
        hint_text="Например, Война и мир",
        expand=True,
    )
    author_field = ft.TextField(
        label="Автор",
        hint_text="Имя и фамилия автора",
        expand=True,
    )
    year_field = ft.TextField(
        label="Год",
        hint_text="1869",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=130,
    )
    price_field = ft.TextField(
        label=f"Цена, {currency}",
        hint_text="500",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=130,
    )
    editing_id = None
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Автор")),
            ft.DataColumn(ft.Text("Год")),
            ft.DataColumn(ft.Text(f"Цена, {currency}")),
            ft.DataColumn(ft.Text("Действия")),
        ],
        rows=[],
        column_spacing=18,
        heading_row_color={ft.ControlState.DEFAULT: "#E8E1D5"},
    )
    status = ft.Text(color="#6B6258", size=13)
    form_title = ft.Text("Добавить книгу", size=20, weight=ft.FontWeight.BOLD)
    books_count = ft.Text(color="#6B6258")

    def clear_form():
        nonlocal editing_id
        editing_id = None
        title_field.value = ""
        author_field.value = ""
        year_field.value = ""
        price_field.value = ""
        form_title.value = "Добавить книгу"

    def refresh_table():
        books_count.value = f"{len(get_books())} книг"
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["title"])),
                    ft.DataCell(ft.Text(item["author"])),
                    ft.DataCell(ft.Text(str(item["year"]))),
                    ft.DataCell(ft.Text(f'{item["price"]} {currency}')),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    tooltip="Редактировать",
                                    on_click=lambda _, book=item: start_edit(book),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    tooltip="Удалить",
                                    icon_color="#A34437",
                                    on_click=lambda _, book_id=item["id"]: remove_book(book_id),
                                ),
                            ],
                            spacing=0,
                        )
                    ),
                ]
            )
            for item in get_books()
        ]
        page.update()

    def start_edit(book):
        nonlocal editing_id
        editing_id = book["id"]
        title_field.value = book["title"]
        author_field.value = book["author"]
        year_field.value = str(book["year"])
        price_field.value = str(book["price"])
        form_title.value = "Редактировать книгу"
        status.value = "Измените данные и нажмите «Сохранить»."
        page.update()

    def remove_book(book_id):
        delete_book(book_id)
        status.value = "Книга удалена."
        refresh_table()

    def save_book(_):
        nonlocal editing_id
        if not all((title_field.value, author_field.value, year_field.value, price_field.value)):
            status.value = "Заполните все поля."
            page.update()
            return

        try:
            year = int(year_field.value)
            price = int(price_field.value)
        except ValueError:
            status.value = "Год и цена должны быть числами."
            page.update()
            return

        if editing_id is None:
            add_book(title_field.value, author_field.value, year, price)
            status.value = "Книга добавлена."
        else:
            update_book(editing_id, title_field.value, author_field.value, year, price)
            status.value = "Изменения сохранены."

        clear_form()
        refresh_table()

    page.add(
        ft.Container(
            width=800,
            height=800,
            padding=ft.Padding(left=42, right=42, top=34, bottom=34),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("BOOKS", size=12, weight=ft.FontWeight.BOLD, color="#A34437"),
                                    ft.Text("Моя библиотека", size=32, weight=ft.FontWeight.BOLD, color="#28231F"),
                                    ft.Text("Управляйте своей коллекцией книг", size=14, color="#6B6258"),
                                ],
                                spacing=4,
                            ),
                            ft.Container(expand=True),
                            ft.Icon(ft.Icons.LOCAL_LIBRARY_OUTLINED, size=48, color="#A34437"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=30, color="transparent"),
                    ft.Container(
                        padding=20,
                        bgcolor="#FFFDF9",
                        border_radius=12,
                        content=ft.Column(
                            [
                                form_title,
                                ft.Row([title_field, author_field]),
                                ft.Row(
                                    [
                                        year_field,
                                        price_field,
                                        ft.Container(expand=True),
                                        ft.OutlinedButton("Очистить", icon=ft.Icons.CLEAR, on_click=lambda _: (clear_form(), page.update())),
                                        ft.FilledButton("Сохранить", icon=ft.Icons.SAVE_OUTLINED, on_click=save_book),
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                status,
                            ],
                            spacing=14,
                        ),
                    ),
                    ft.Row(
                        [
                            ft.Text("Все книги", size=22, weight=ft.FontWeight.BOLD, color="#28231F"),
                            ft.Container(expand=True),
                            books_count,
                        ],
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor="#FFFDF9",
                        border_radius=12,
                        padding=10,
                        content=ft.Column([table], scroll=ft.ScrollMode.AUTO),
                    ),
                ],
                spacing=18,
                expand=True,
            ),
        )
    )
    refresh_table()


if __name__ == "__main__":
    ft.run(main)
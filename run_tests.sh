#!/bin/bash

echo $(poetry run pytest tests/test_admin.py::test_admin_categories_crud)
echo $(poetry run pytest tests/test_admin.py::test_admin_posts_crud)
echo $(poetry run pytest tests/test_admin.py::test_admin_users_crud_list_get_update)
echo $(poetry run pytest tests/test_auth.py::test_register_login_refresh_me_flow)
echo $(poetry run pytest tests/test_public.py::test_public_posts_and_categories)

echo "Finish"
sleep 2
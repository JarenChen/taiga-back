# -*- coding: utf-8 -*-
# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.core.management.base import BaseCommand
from taiga.projects.choices import BLOCKED_BY_NONPAYMENT
from taiga.projects.models import Project


class Command(BaseCommand):
    help = "Block projects"

    def add_arguments(self, parser):
        parser.add_argument("owner_usernames",
                            nargs="+",
                            help="<owner_usernames owner_usernames ...>")

        parser.add_argument("--only-private-projects",
                            dest="only_private_projects",
                            action="store_true")

    def handle(self, *args, **options):
        owner_usernames = options["owner_usernames"]
        projects = Project.objects.filter(owner__username__in=owner_usernames)
        if options["only_private_projects"]:
            projects = projects.filter(is_private=True)

        projects.update(blocked_code=BLOCKED_BY_NONPAYMENT)

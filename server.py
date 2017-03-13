# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Teresa Abad Rueda
#


import web
import socketserver  #se pasa de web.py aqui pqq solo se utiliza aqui

PORT=8000 #Puerto por defecto

##WEB SERVER

Handler = web.testHTTPRequestHandler  #cojo la clase del fichero web.py
httpd = socketserver.TCPServer(("", PORT), Handler)
#httpd =objeto que ejecuta un metodo para siempre
#HAndler= es un objeto que es una instancia de es
#cada vez que llega un cliente se crea un handler e interactua con el

#se crean objetos handler para poder crear conexiones con los clientes, los handler son objetos basados en la clase Handler que es como nos indica como tratar a esos cli
print("serving at port", PORT)
httpd.serve_forever()

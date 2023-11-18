import requests
import pickle
import uuid
from Student import Student
from Professor import Professor
from Post import Post
from Estadisticas import Estadisticas

class App:
  def __init__(self):
    self.usuarios = []
    self.posts = []

  def precargar_datos(self):
    respuesta_usuarios = requests.get('https://github.com/Algoritmos-y-Programacion-2223-3/api-proyecto/blob/main/users.json')
    datos_usuarios = respuesta_usuarios.json()
    for usuario in datos_usuarios:
      nuevo_usuario1 = Student(usuario['ID'], usuario['firstName'], usuario['lastName'], usuario['email'], usuario['username'], usuario['major'], usuario['following'])
      nuevo_usuario2 = Professor(usuario['ID'], usuario['firstName'], usuario['lastName'], usuario['email'], usuario['username'], usuario['department'], usuario['following'])
      self.usuarios.append(nuevo_usuario1)
      self.usuarios.append(nuevo_usuario2)

    respuesta_posts = requests.get('https://github.com/Algoritmos-y-Programacion-2223-3/api-proyecto/blob/main/posts.json')
    datos_posts = respuesta_posts.json()
    for post in datos_posts:
      usuario = next((u for u in self.usuarios if u.id == post['publisher']), None)
      if usuario:
        nuevo_post = Post(usuario, post['multimedia'], post['caption'], post['tags'])
        self.posts.append(nuevo_post)

  def registrar_usuario(self, id, firstName, lastName, email, username, following, major=None, department=None): 
    if major: 
      nuevo_usuario = Student(id, firstName, lastName, email, username, following, major)
    elif department:  
      nuevo_usuario = Professor(id, firstName, lastName, email, username, following, department)
    else:
      raise ValueError("Debe ser major o department")
    self.usuarios.append(nuevo_usuario)
    print("Usuario ingresado correctamente")

  def registrar_post(self, usuario, multimedia, descripcion, hashtag):
    nuevo_post = Post.registrar_nuevo_post(usuario, multimedia, descripcion, hashtag)
    self.posts.append(nuevo_post)
    usuario.publicaciones.append(nuevo_post)

  def seguir_usuario(self, usuario, otro_usuario):
    usuario.seguir(otro_usuario)

  def aprobar_seguimiento(self, usuario, otro_usuario):
    usuario.aprobar_seguimiento(otro_usuario)

  def dejar_de_seguir_usuario(self, usuario, otro_usuario):
    usuario.dejar_de_seguir(otro_usuario)

  def comentar_post(self, usuario, post, comentario):
    usuario.comentar_post(post, comentario)

  def like_post(self, usuario, post):
    usuario.like_post(post)

  def delete_post(self, usuario, comentario):
    usuario.eliminar_comentario(comentario)

  def ver_perfil(self, usuario, otro_usuario):
    return otro_usuario.mostrar_perfil()

  def eliminar_post(self, administrador, post):
    administrador.eliminar_post(post, self.posts)

  def eliminar_comentario(self, administrador, comentario):
    administrador.eliminar_comentario(comentario, self.posts)

  def eliminar_usuario(self, administrador, usuario):
    administrador.eliminar_usuario(usuario, self.usuarios)

  def generar_informe_publicaciones(self):
    return Estadisticas.informe_publicaciones(self.usuarios)

  def generar_informe_interacciones(self):
    return Estadisticas.informe_interacciones(self.usuarios, self.posts)

  def generar_informe_moderacion(self):
    return Estadisticas.informe_moderacion(self.usuarios, self.posts)

  def graficar_estadisticas(self, estadisticas):
    Estadisticas.graficar_estadisticas(estadisticas)

  def binary_search(self, y, x):
    low = 0
    high = len(y) - 1
    mid = 0
  
    while low <= high:
        mid = (high + low) // 2
        if y[mid] < x:
            low = mid + 1
        elif y[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1
  
  def save_data_usuarios(self):
    with open("usuarios.pickle", "wb+") as f:
        pickle.dump(self.usuarios, f)

  def read_data_usuarios(self):
    try:
      with open("usuarios.pickle", "rb") as f:
        self.usuarios = pickle.load(f)
    except:
      print("No hay datos guardados!")

  def save_data_publicaciones(self):
    with open("posts.pickle", "wb+") as f:
        pickle.dump(self.posts, f)

  def read_data_publicaciones(self):
    try:
      with open("posts.pickle", "rb") as f:
        self.posts = pickle.load(f)
    except:
      print("No hay datos guardados!")
  
  def gestion_perfil(self):
    while True:
      try:
        option = int(input("""¿Que desea hacer?
        1. Registrar usuario
        2. Buscar perfiles
        3. Cambiar informacion de usuario
        4. Borrar datos de la cuenta
        5. Acceder a la cuenta de otra usuario
        6. Salir
        > """))
        if option < 1 or option > 6:
          raise ValueError
      except:
        print("DATO INVALIDO")
        continue

      if option == 1:
        id = uuid.uuid4()
        while True:
          try:
            firstName = input("Ingrese el primer nombre del usuario: ")
            if firstName.isalpha() != True:
              raise ValueError
            break
          except:
            print('El primer nombre debe ser solo letras')

        while True:
          try:
            lastName = input("Ingrese el apellido del usuario: ")
            if lastName.isalpha() != True:
              raise ValueError
            break
          except:
            print('El apellido debe ser solo letras')

        email = input("Ingrese el email del usuario: ")
        username = input("Ingrese el username del usuario: ")
        following = []

        tipo = input("Indique si el usario es un 'Professor' o un 'Student': ")
        if tipo.lower() == "professor":
          department = input("Ingrese el departamento del usuario: ")
          self.registrar_usuario(id, firstName, lastName, email, username, following, "professor", department)
        elif tipo.lower() == "student":
          major = input("Ingrese la carrera del usuario: ")
          self.registrar_usuario(id, firstName, lastName, email, username, following, "student", major)      
      
      elif option == 2:
        filtro = input("Con que filtro deseas buscar el perfil, Username, Carrera o Departamento: ")
        if filtro.title() == "Username":
          username = input("Indique el nombre de usuario que quiere buscar: ")
          resultado1 = self.usuarios[self.binary_search(self.usuarios, username)]
          print(resultado1.show_attr())
        elif filtro.title() == "Carrera":
          major = input("Indique la carrera que quiere buscar: ")
          self.buscar_estudiantes(self.usuarios, filtro, major)
        elif filtro.title() == "Departamento":
          department = input("Indique el departamento que quiere buscar: ")
          self.buscar_profesores(self.usuarios, filtro, department)
      elif option == 3:
        tipo = input("Indique si el usario es un 'Professor' o un 'Student':")
        cambio = input("indica que informacion quieres cambiar: ")
        if tipo.lower() == "student":
          self.cambiar_informacion_estudiante(cambio)
        elif tipo.lower() == "professor":
          self.cambiar_informacion_profesor(cambio)
      elif option == 4:
        type = input("Indique el tipo de usuario, Professor o Student: ")
        if type.lower() == "student":
          self.borrar_estudiante() 
        elif type.lower() == "professor":
          self.borrar_estudiante()
      elif option == 5:
          user = input("Ingrese el username del que desea ver sus posts: ")
          for usuario in self.usuarios:
            if usuario.username == user:
              for post in usuario.posts:
                print(post.show_attr())
            else:
              print("El usuario no existe")
      else:
        break

  def gestion_multimedia(self):
    while True:
      try:
        opcion = int(input("""¿Que desea hacer?
        1. Registrar los datos del post
        2. Ver posts de otros usuarios
        3. Buscar post
        4. Salir
        > """))
        if opcion < 1 or opcion > 4:
          raise ValueError
      except:
        print("DATO INVALIDO")
        continue

      if opcion == 1:
        usuario = input("Indique el usuario que registra el comentario")
        multimedia = input("Indique el tipo de multimedia, Foto o Video: ")
        descripcion = input("Ingrese la descripcion del post: ")
        hashtag = input("Ingrese el hashtag del post: ")

        self.registrar_post(usuario, multimedia, descripcion, hashtag)

      elif opcion == 2:
        posts = [
            post
            for post in self.posts
            if post.usuario == usuario
        ]
        for post in posts:
            print(post)
      elif opcion == 3:
        filtro = input("Indique el filtro con el que desea buscar post: ")
        valor = input("Indique el valor: ")
        posts = self.buscar_posts(self.posts, filtro, valor)
        for post in posts:
            print(post)
      else:
        break

  def gestion_interacciones(self):
    while True:
      try:
        opcion = int(input("""¿Que desea hacer?
        1. Seguir a un usuario
        2. Dejar de seguir a un usuario
        3. Comentar un post
        4. Dar like a un post
        5. Eliminar un post
        6. Acceder a perfil de otro usuario
        7. Salir
        > """))
        if opcion < 1 or opcion > 7:
          raise ValueError
      except:
        print("DATO INVALIDO")
        continue

      if opcion == 1:
        usuario = input("Indique su usuario")
        for user in self.usuarios:
          if user.username == usuario:
            otro_usuario = input("Ingrese el usuario que desea seguir:")
            if user.username == otro_usuario:
              self.seguir_usuario(user, otro_usuario)
            else:
              print("No encontrado")
          else:
            print("No encontrado")

      elif opcion == 2:
        usuario = input("Indique su usuario: ")
        for user in self.usuarios:
          if user.username == usuario:
            otro_usuario = input("Ingrese el usuario que desea dejar de seguir:")
            if user.username == otro_usuario:
              self.dejar_de_seguir_usuario(user, otro_usuario)
            else:
              print("No se encontro")
            
      elif opcion == 3:
        user = input("Indique su usuario: ")
        for u in self.usuarios:
          if u.username == user:
            post = input("Busca el post: ")
            for p in self.posts:
              if p.usuario == user and p.descripcion == post:
                comentario = input("Ingrese su comentario: ")
                self.comentar_post(usuario, p, comentario)

      elif opcion == 4:
        usuario = input("Indique su usuario: ")
        for user in self.usuarios:
          if user.username == usuario:
            post = input("Busca el post: ")
            for p in self.posts:
              if p.autor == usuario and p.titulo == post:
                self.like_post(usuario, p)
              else:
                print("Mo encontrado")
          else:
            print("No encontrado")
      
      elif opcion == 5:
        usuario = input("Indique su usuario: ")
        for user in self.usuarios:
          if user.username == usuario:
            post = input("Busca el post: ")
            for p in self.posts:
              if p.autor == usuario and p.titulo == post:
                self.delete_post(p)
              else:
                print("No encontrado")
          else:
            print("No encontraddo")
      elif opcion == 6:
        usuario = input("Indique su usuario: ")
        for user in self.usuarios:
          if user.username == usuario:
            otro_usuario = input("Ingrese el usuario que desea ver el perfil:")
            if user.username != otro_usuario:
              perfil = self.ver_perfil(user, otro_usuario)
              print(perfil)
            else:
              print("No se encontro")
          else:
            print("No se encontro")
      else:
        break

  def gestion_moderacion(self):
    while True:
      try:
        opcion = int(input("""¿Que desea hacer?
        1. Eliminar post
        2. Eliminar comentario
        3. Eliminar un usuario que infringido múltiples veces las reglas 
        4. Salir
        > """))
        if opcion < 1 or opcion > 4:
          raise ValueError
      except:
        print("DATO INVALIDO")
        continue

      if opcion == 1:
        administrador = input("Indique el usuario administrador: ")
        for user in self.usuarios:
          if user.username == administrador:
            post = input("Ingrese el post que desea eliminar: ")
            for p in self.posts:
              if p.descripcion == post:
                self.eliminar_post(administrador, post)
              else:
                print("No se encontro")
          else:
            print("No se encontro")
      elif opcion == 2:
        self.eliminar_comentario()
      elif opcion == 3:
        self.eliminar_usuario()
      else:
        break

  def indicadores_gestion(self):
    while True:
      try:
        opcion = int(input("""¿Que desea hacer?
        1. Generar informes de publicaciones
        2. Generar informes de interacción
        3. Generar informes de moderación
        4. Generar graficas de estadisticas
        5. Salir
        > """))
        if opcion < 1 or opcion > 5:
          raise ValueError
      except:
        print("DATO INVALIDO")
        continue

      if opcion == 1:
        self.generar_informe_publicaciones()
      elif opcion == 2:
        self.generar_informe_interacciones()
      elif opcion == 3:
        self.generar_informe_moderacion()
      elif opcion == 4:
        estadisticas = input("")
        self.graficar_estadisticas(estadisticas)
      else:
        break


  
  def start(self):
    self.read_data_usuarios()
    self.read_data_publicaciones()
    print("\nBienvenido a Metrogram!")
    while True:
      try:
        menu = int(input("""¿Que desea hacer?
          1. Gestion de perfil
          2. Gestion de multimedia
          3. Gestion de interacciones
          4. Gestion de moderacion
          5. Estadisticas
          6. Salir
          > """))
        if menu < 1 or menu > 6:
            raise ValueError
      except:
        print("DATO INVALIDO")
        continue

      if menu == 1:
        self.gestion_perfil()
      elif menu == 2:
        self.gestion_multimedia()
      elif menu == 3:
        self.gestion_interacciones()
      elif menu == 4:
        self.gestion_moderacion()
      elif menu == 5:
        self.indicadores_gestion()
      else:
        self.save_data_usuarios()
        self.save_data_publicaciones()
        print("Gracias por usar Metrogram!")
        break

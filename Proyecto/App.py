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
        usuario.publicaciones.append(nuevo_post)

  def registrar_usuario(self, id, firstName, lastName, email, username, following, major=None, department=None): 
    if major: 
      nuevo_usuario = Student(id, firstName, lastName, email, username, following, major)
    elif department:  
      nuevo_usuario = Professor(id, firstName, lastName, email, username, following, department)
    else:
      raise ValueError("Debe ser major o department")
    self.usuarios.append(nuevo_usuario)

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

  def eliminar_comentario(self, usuario, comentario):
    usuario.eliminar_comentario(comentario)

  def ver_perfil(self, usuario, otro_usuario):
    return usuario.ver_perfil(otro_usuario)

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
    Estadisticas.graficar_estadisticas(estadisticas)]
  
  def save_data(self):
    with open("users.pickle", "wb+") as f:
        pickle.dump(self.users, f)

  def read_data(self):
    try:
        with open("employees.pickle", "rb") as f:
            self.employees = pickle.load(f)
    except:
        print("No hay datos guardados!")

  
  
  def gestion_perfil(self):
    while True:
      try:
        option = int(input("""¿Que desea hacer?
        1) Registrar usuario
        2) Buscar perfiles
        3) Cambiar informacion de usuario
        4) Borrar datos de la cuenta
        5) Acceder a la cuenta de otra usuario
        6) Salir
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
        while True:
          eleccion = input("Indique si quieres continuar agregar un seguidor, (S)i o (N)o: ")
          if eleccion == "S":
            following.append(uuid.uuid4())
          elif eleccion == "N":
            break
          else:
            print("Ingrese una opción válida")

        while True:
          try:
            type = input("Indique si el usario es un 'Professor' o un 'Student': ")
            if type.lower() != 'professor' or type.lower() != 'student':
              raise ValueError
            break
          except:
            print('El tipo debe ser Professor o Student')

        while True:
          if type == "professor":
            department = input("Ingrese el departamento del usuario: ")
          elif type == "student":
            major = input("Ingrese la carrera del usuario: ")
        
        self.registrar_usuario(self, id, firstName, lastName, email, username, following, major, department)
      
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
        cambio = input("indica que informacion quieres cambiar: ")
      elif option == 4:
        type = input("Indique el tipo de usuario, Professor o Student: ")
        if type == "professor":
          id = input("Indique el ID del estudiante a eliminar: ")
          for user in self.user:
            if user.id == id:
              
      elif option == 5:
        self.ver_otro_usuario()
      else:
        break

  def gestion_multimedia(self):
    while True:
      try:
        opcion = int(input("""¿Que desea hacer?
        1) Registrar los datos del post
        2) Ver posts de otros usuarios
        3) Buscar post
        4) Salir
        > """))
        if opcion < 1 or opcion > 4:
          raise ValueError
      except:
        print("DATO INVALIDO")
        continue

      if opcion == 1:
        self.registrar_post()
      elif opcion == 2:
        self.ver_posts()
      elif opcion == 3:
        self.buscar_post()
      else:
        break

  def gestion_interacciones(self):
    while True:
      try:
        opcion = int(input("""¿Que desea hacer?
        1) Seguir a un usuario
        2) Dejar de seguir a un usuario
        3) Comentar post
        4) Dar like a un post
        5) Eliminar un post
        6) Acceder a perfil de otro usuario
        7) Salir
        > """))
        if opcion < 1 or opcion > 7:
          raise ValueError
      except:
        print("DATO INVALIDO")
        continue

  def gestion_moderacion(self):
    while True:
      try:
        opcion = int(input("""¿Que desea hacer?
        1)  Eliminar post
        2) Eliminar comentario
        3) Eliminar un usuario que infringido múltiples veces las reglas 
        4) Salir
        > """))
        if opcion < 1 or opcion > 4:
          raise ValueError
      except:
        print("DATO INVALIDO")
        continue

      if opcion == 1:
        self.eliminar_post()
      elif opcion == 2:
        self.eliminar_comentario()
      elif opcion == 3:
        self.eliminar_usuario()
      else:
        break

  def start(self):
      self.save_data()
      print("\nBienvenido a Metrogram!")
      while True:
        try:
          menu = int(input("""¿Que desea hacer?
          1) Gestion de perfil
          2) Gestion de multimedia
          3) Gestion de interacciones
          4) Gestion de moderacion
          5) Estadisticas
          6) Salir
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
          self.estadisticas()
        else:
          self.save_data()
          print("Gracias por usar Metrogram!")
          break

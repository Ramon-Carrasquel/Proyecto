from User import User

class Student(User):
  def __init__(self, id, firstName, lastName, email, username, following, major):
    super().__init__(id, firstName, lastName, email, username, following)
    self.type = "student"  
    self.major = major

  def show_attr(self):
    return f"""
    ID: {self.id}
    Primer Nombre: {self.firstName}
    Apellido: {self.lastName}
    Email: {self.email}
    Nombre de usuario: {self.username}
    Publicaciones: {self.posts}
    Siguiendo: {self.show_following()}
    """
  
  @staticmethod
  def registrar_estudiante(id, firstName, lastName, email, username, following, major):
    return Student(id, firstName, lastName, email, username, following, major)

  @staticmethod
  def buscar_estudiantes(usuarios, filtro, valor):
      return [usuario for usuario in usuarios if getattr(usuario, filtro) == valor]
  
  def cambiar_informacion_estudiante(self, id=None, firstName=None, lastName=None, email=None, username=None, following=None, major=None):
    if id:
      self.id = id
    if firstName:
      self.firstName = firstName
    if lastName:
      self.lastName = lastName
    if email:
      self.email = email
    if username:
      self.username = username
    if following:
      self.following = following
    if major:
      self.major = major
    
  def borrar_estudiante(self):
    del self
  
  def seguir(self, otro_usuario):
    if self.major == otro_usuario.major:
        self.following.append(otro_usuario)
        otro_usuario.following.append(self)
    else:
        otro_usuario.solicitudes.append(self)
  
  
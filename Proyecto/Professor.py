from User import User

class Professor(User):
  def __init__(self, id, firstName, lastName, email, username, following, department):
    super().__init__(id, firstName, lastName, email, username, following)
    self.type = "professor"
    self.department = department

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
  def registrar_profesor(id, firstName, lastName, email, username, following, department):
    return Professor(id, firstName, lastName, email, username, following, department)

  @staticmethod
  def buscar_profesores(usuarios, filtro, valor):
      return [usuario for usuario in usuarios if getattr(usuario, filtro) == valor]
  
  def cambiar_informacion_profesor(self, id=None, firstName=None, lastName=None, email=None, username=None, following=None, department=None):
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
    if department:
      self.department = department
  
  def borrar_profesor(self):
    del self
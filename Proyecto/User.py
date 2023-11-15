from Comment import Comment

class User:
  def __init__(self, id, firstName, lastName, email, username, following):
    self.id = id
    self.firstName = firstName
    self.lastName = lastName
    self.email = email
    self.username = username
    self.following = following
    self.seguidores = []
    self.solicitudes = []
    self.posts = []

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

  def show_following(self):
    following = ""
    for user in self.following:
      following += user.show_attr()
  
    return following


  def aprobar_seguimiento(self, otro_usuario):
    if otro_usuario in self.solicitudes:
        self.solicitudes.remove(otro_usuario)
        self.seguidores.append(otro_usuario)
        otro_usuario.seguidos.append(self)

  def dejar_de_seguir(self, otro_usuario):
    if otro_usuario in self.following:
        self.following.remove(otro_usuario)
        otro_usuario.following.remove(self)

  def comentar_post(self, user, post, comment, publish_date):
    nuevo_comentario = Comment(user, post, comment, publish_date)
    post.comentarios.append(nuevo_comentario)

  def like_post(self, post):
    if self in post.likes:
        post.likes.remove(self)
    else:
        post.likes.append(self)

  def ver_perfil(self, otro_usuario):
    return otro_usuario.mostrar_perfil()

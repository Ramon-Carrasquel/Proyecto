from User import User

class Administrator(User):

  def __init__(self, id, firstName, lastName, email, username, posts, following):
    super().__init__(id, firstName, lastName, email, username, posts, following)

  def eliminar_post(self, post, lista_posts):
    if post in lista_posts:
        lista_posts.remove(post)

  def eliminar_comentario(self, comentario, lista_posts):
    for post in lista_posts:
        if comentario in post.comentarios:
            post.comentarios.remove(comentario)

  def eliminar_usuario(self, usuario, lista_usuarios):
    if usuario in lista_usuarios:
        lista_usuarios.remove(usuario)
class Comment:
  def __init__(self, user, post, comment, publish_date):
    self.user = user
    self.post = post
    self.comment = comment
    self.publish_date = publish_date

  def show_attr(self):
    return f"""
    Usuario: {self.user}
    Publicacion: {self.post}
    Comentario: {self.comment}
    Fecha de publicación: {self.publish_date}
    """
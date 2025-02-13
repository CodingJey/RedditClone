

class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey('threads.thread_id'), index=True)
    poster_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    content = Column(String)
    post_date = Column(Date)
    rating = Column(Integer, default=0)
    thread = relationship("Thread", back_populates="posts")
    poster = relationship("User", back_populates="posts")

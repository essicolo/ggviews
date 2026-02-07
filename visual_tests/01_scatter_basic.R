library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  labs(title='Sepal Length vs Width', x='Sepal Length (cm)', y='Sepal Width (cm)')
ggsave('01_scatter_basic.png', width=5, height=4)

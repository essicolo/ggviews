library(ggplot2)
ggplot(iris, aes(x=Species, y=Sepal.Length)) +
  geom_boxplot() +
  coord_flip() +
  labs(title='Horizontal Boxplot')
ggsave('14_coord_flip.png', width=5, height=4)

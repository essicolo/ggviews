library(ggplot2)
ggplot(iris, aes(x=Sepal.Length)) +
  geom_density() +
  labs(title='Sepal Length Density', x='Sepal Length', y='Density')
ggsave('08_density.png', width=5, height=4)

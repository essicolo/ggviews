library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width, color=Species)) +
  geom_point() +
  labs(title='Iris by Species')
ggsave('02_scatter_color.png', width=6, height=4)

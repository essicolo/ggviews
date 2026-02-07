library(ggplot2)
ggplot(iris, aes(x=Species, y=Sepal.Length)) +
  geom_boxplot() +
  labs(title='Sepal Length by Species', x='Species', y='Sepal Length')
ggsave('07_boxplot.png', width=5, height=4)

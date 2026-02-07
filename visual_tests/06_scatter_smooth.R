library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  geom_smooth(method='lm') +
  labs(title='Sepal Dimensions with Linear Fit')
ggsave('06_scatter_smooth.png', width=5, height=4)

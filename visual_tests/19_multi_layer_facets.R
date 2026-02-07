library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  geom_smooth(method='lm') +
  facet_wrap(~Species) +
  labs(title='Linear Fits by Species')
ggsave('19_multi_layer_facets.png', width=9, height=4)

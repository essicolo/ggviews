library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  facet_wrap(~Species) +
  labs(title='Faceted by Species')
ggsave('10_facet_wrap.png', width=9, height=4)

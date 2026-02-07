library(ggplot2)
library(gghighlight)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  gghighlight(Species == 'setosa') +
  labs(title='Highlighted: setosa')
ggsave('18_highlight.png', width=5, height=4)

library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  theme_classic() +
  labs(title='Classic Theme')
ggsave('16_theme_classic.png', width=5, height=4)

library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  theme_minimal() +
  labs(title='Minimal Theme')
ggsave('15_theme_minimal.png', width=5, height=4)

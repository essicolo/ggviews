library(ggplot2)
ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) +
  geom_point() +
  labs(title='Main Title Here',
       x='X Axis Label (units)',
       y='Y Axis Label (units)')
ggsave('20_labels_title.png', width=5, height=4)

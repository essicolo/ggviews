library(ggplot2)
ggplot(iris, aes(x=Sepal.Length)) +
  geom_histogram(bins=15) +
  labs(title='Distribution of Sepal Length', x='Sepal Length', y='Count')
ggsave('04_histogram.png', width=5, height=4)

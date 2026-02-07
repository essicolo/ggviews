library(ggplot2)
df <- data.frame(x=0:19, y=cumsum(rnorm(20)))
ggplot(df, aes(x=x, y=y)) +
  geom_line() +
  labs(title='Random Walk', x='Step', y='Value')
ggsave('05_line.png', width=5, height=4)

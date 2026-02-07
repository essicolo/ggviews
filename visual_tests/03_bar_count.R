library(ggplot2)
ggplot(tips, aes(x=day)) +
  geom_bar() +
  labs(title='Tips by Day', x='Day of Week', y='Count')
ggsave('03_bar_count.png', width=5, height=4)

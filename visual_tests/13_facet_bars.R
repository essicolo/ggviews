library(ggplot2)
ggplot(tips, aes(x=day)) +
  geom_bar() +
  facet_wrap(~sex) +
  labs(title='Day counts by Sex')
ggsave('13_facet_bars.png', width=8, height=4)

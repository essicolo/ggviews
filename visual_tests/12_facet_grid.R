library(ggplot2)
ggplot(tips, aes(x=total_bill, y=tip)) +
  geom_point() +
  facet_grid(sex ~ smoker) +
  labs(title='Tips: Sex vs Smoker Grid')
ggsave('12_facet_grid.png', width=7, height=5)

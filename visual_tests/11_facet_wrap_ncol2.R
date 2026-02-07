library(ggplot2)
ggplot(tips, aes(x=total_bill, y=tip)) +
  geom_point() +
  facet_wrap(~day, ncol=2) +
  labs(title='Tips by Day (2 columns)')
ggsave('11_facet_wrap_ncol2.png', width=8, height=6)

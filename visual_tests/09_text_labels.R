library(ggplot2)
df <- data.frame(x=c(1,2,3,4,5), y=c(2,4,3,5,1),
                 name=c('Alpha','Beta','Gamma','Delta','Epsilon'))
ggplot(df, aes(x=x, y=y, label=name)) +
  geom_point() +
  geom_text() +
  labs(title='Points with Labels')
ggsave('09_text_labels.png', width=5, height=4)

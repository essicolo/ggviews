library(ggplot2)
library(ggrepel)
df <- data.frame(x=c(1,2,3,4,5), y=c(2,4,3,5,1),
                 name=c('Alpha','Beta','Gamma','Delta','Epsilon'))
ggplot(df, aes(x=x, y=y, label=name)) +
  geom_point() +
  geom_text_repel() +
  labs(title='Repelled Labels')
ggsave('17_repel_labels.png', width=5, height=4)

library(googleAnalyticsR)

#authenticate with your Google Analytics login

ga_auth()
search()

df <- dim_filter(dimension="pagePath", operator= "REGEXP",expressions="/collection/(heart-failure|clinical-cardiology|coronary-peripheral-structural-interventions|rhythm-disorders|appropriate-use-criteria|clinical-alerts|competence-and-training-statements|data-standards|expert-consensus-documents|guidelines|health-policy-statements|other-guidelines|performance-measures|survey-and-data-reports)")
df2 <- dim_filter(dimension="pagePath",operator="REGEXP",expressions="sso",not=TRUE)

fc2 <- filter_clause_ga4(list(df,df2),operator="AND")

jaccCollectionsPages <- google_analytics_4(132933676,
                                           date_range=c("2017-01-01",
                                                        "2017-07-31"),
                                           metrics=c("pageviews"),
                                           dimensions=c("pagePath","pagePathLevel2"),
                                           dim_filters=fc2,
                                           anti_sample=TRUE)

write.csv(jaccCollectionsPages,file="jaccCollections.csv")

# Dockerfile
FROM --platform=linux/arm64/v8 selenium/standalone-chrome

COPY start-selenium-grid.sh /

CMD ["/start-selenium-grid.sh"]

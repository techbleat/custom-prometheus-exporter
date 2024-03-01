# Project demonstrates how to build Promethues Exporter
## In this case, we use Python extract Premier League (Arsenal) players' stats from a third party website, ingest into Prometheus and display on Grafana

### Source data : https://fbref.com/en/comps/9/Premier-League-Stats

![plot](./prom-image.png)


## Set Up Requirements on a (Amazon) Linux node ( If you dont want to run on your local PC)
```
sudo yum update -y 
sudo amazon-linux-extras install docker 
sudo yum install docker git -y
sudo service docker start 
sudo usermod -a -G docker ec2-user 
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Run App
```
git clone https://github.com/techbleat/premierleague_footy.git
cd premierleague_footy/
docker-compose up -d --build
#sudo docker-compose up -d --build
```

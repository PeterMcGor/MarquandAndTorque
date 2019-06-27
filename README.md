## Docker Torque

#### Introduction

This image runs the Torque scheduler and a single worker on a Ubuntu host. One user is provided for submission of jobs. --> This is from https://github.com/neilav/docker-torque

I have included Andre Marquand work for nispat --> https://github.com/amarquand/nispat

#### Build

`docker build -t torque .`

#### Run

`docker run -h master --privileged -it torque bash`

#### Submit Jobs

`qsub -P batchuser`

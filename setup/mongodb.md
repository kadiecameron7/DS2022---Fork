# Set up your own MongoDB Atlas Cluster in the Cloud

This course will be using MongoDB Atlas, a cloud-based Mongo service, for hands-on exercises.

## 1. Sign up for MongoDB Atlas

Follow the instructions in the **[How To video](https://www.youtube.com/watch?v=5-tIfDCb-T4)** for setup.

I recommend using a Google account to **[create your Atlas MongoDB Cluster](https://www.mongodb.com/cloud/atlas/register)**. But you can create an account with any valid email address.

## 2. Update the IP access list

In order to reach the MongoDB Atlas cloud service from the UVA HPC cluster (or other locations on grounds), you have to update the list of IP addresses allowed to connect to the service. This is called `whitelisting`.

1. In the MongoDB Atlas web interface, click on `Database & Network Access` on the left-hand sidebar (grouped under `Security`).
2. On the next screen click on `IP Access List`.
3. Click the `+Add IP ADDRESS` button and add the `128.143.0.0/16` address as `UVA Block 1`. Repeat this step for the `199.111.0.0/16` address as `UVA Block 2`. In CIDR notation, the number after the slash (e.g. `/16`) is the prefix length: it indicates how many bits define the network, so `/16` allows all IPs in that network block (e.g. 128.143.0.0 through 128.143.255.255).

The IP Access list should look similar to this:

![MongoDB Atlas IP access list](../docs/images/mongodb-atlas-ip.png)

Your address entry next to `Created as part of the Auto Setup process` is likely different. The `Home network` address is not needed unless you want to access the MongoDB Atlas cluster from off-grounds.

## 3. Get Connection String (URL)

1. In the MongoDB Atlas web interface, click on `Database` > `Clusters` (left side menu). In this case the cluster is named `ds2002`. You may have chosen a different name during setup, which is fine.

![Mongo DB Atlas Cluster](../docs/images/mongodb-atlas-cluster.png)

2. Click on the `Connect` button of your cluster and select `Shell - Quickly add & update data using MongoDB's Javascript command-line interface`. This will give you a `connection string` similar to this:

```bash
mongosh "mongodb+srv://ds2002.tmwdrjn.mongodb.net/" --apiVersion 1 --username <username>
```

The `connection URL` is the part between the pair of `"`. In this case: `mongodb+srv://ds2002.tmwdrjn.mongodb.net/`, **yours will be different.**

- If the URL extends beyond `...mongodb.net/`, delete it from the connection string.
- Replace `<username>` with the user you created when you signed up for MongoDB Atlas.

## 4. Save Connection String

Open your `~/.bashrc` (or `~/.zshrc`) and add the following export statements:

```bash
export MONGODB_ATLAS_URL="<YOUR_CONNECTION_URL>"  # e.g. mongodb+srv://ds2002.tmwdrjn.mongodb.net/
export MONGODB_ATLAS_USER="<YOUR_USERNAME>"
export MONGODB_ATLAS_PWD="<YOUR_PASSWORD>"
```

## Install the `mongosh` client on your computer

**Mac users:**

1. Open a terminal.
2. Run:

```bash
brew install mongosh
```

3. Confirm installation:

```bash
mongosh --version
```

**WSL/Linux (Ubuntu):**

1. See which Ubuntu you have:

```bash
cat /etc/os-release
```

Look at the `VERSION_ID` line (for example `22.04`, `24.04`, or `26.04`).

2. Pick one option below.

### Option A — install with package manager (Ubuntu 22.04 or 24.04)

```bash
# 1. Import MongoDB's public GPG key
wget -qO- https://www.mongodb.org/static/pgp/server-8.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-8.0.asc

# 2. Add MongoDB's package source
# Ubuntu 24.04:
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.3 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.3.list
# Ubuntu 22.04: use the same command, but change noble to jammy

# 3. Install mongosh
sudo apt-get update
sudo apt-get install -y mongodb-mongosh
```

If step 1 complains that `gnupg` is missing, run `sudo apt-get install -y gnupg` and try again.

Confirm:

```bash
mongosh --version
```

**If install fails, it may be due to version drift between your Ubuntu version and MongoDB’s package sources. Try the install script in *Option B***.

### Option B — install from script (Ubuntu 26.04, or if Option A fails)

MongoDB does not provide package-manager install for Ubuntu 26.04. Do **not** reuse the 24.04 package lines on 26.04; that does not work. Use the script instead.

From the course `setup` folder:

```bash
./install_mongosh.sh && source ~/.bashrc
mongosh --version
```

This downloads `mongosh` into `~/.local/bin` and adds that folder to your `PATH` in `~/.bashrc`. No `sudo` needed.

For other Linux distros, see the official [mongosh install docs](https://www.mongodb.com/docs/mongodb-shell/install/).

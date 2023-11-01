# airflow_k8ns
Easy deployment for Airflow into Kubernetes using HELM as base (Dcoker Desktop for testing).


# Pulling HELM apache-airflow repo  (base templates)
    helm repo add apache-airflow https://airflow.apache.org

# Creating the deployment using as base the apache/airflow Docker image
    helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace 
  
  * This command will create all the deploymente into the Kubernetes Cluster. If the namespace "airflow" doesn't exist it will be created.

# Creating the deployment using as base a personal Docker image
    helm upgrade --install airflow apache-airflow/airflow \
    --set images.airflow.repository={dockerHubRepo/mageName}\
    --set images.airflow.tag={tag} \
    --namespace airflow --create-namespace
    
  * This command will create all the deploymente into the Kubernetes Cluster with the image used in the parameters. If the namespace "airflow" doesn't exist it will be created.

# Updating the release environment using Values.yaml
In case you want to update the release and change some values within the environment variables you can run the next command.
  helm upgrade airflow apache-airflow/airflow --debug -f ./config/values.yaml --namespace airflow

  * The values.yaml file should looks like this simple example:
    
  ```
  env:
    - name: AIRFLOW__CORE__LOAD_EXAMPLES
      value: 'true'"
  ```

# Debuggin and depper understanding about the YAML files strcuture used for the realease
In case you want to take a look deeper in your current realese yaml files, you can run the next script:
  ```sh ./get_yamls.sh```
* The script file looks like:
  ```
  NAMESPACE="airflow"

  kubectl get all -n $NAMESPACE -o yaml > resources.yaml
  kubectl get configmap -n $NAMESPACE -o yaml > configmaps.yaml
  kubectl get secret -n $NAMESPACE -o yaml > secrets.yaml
  kubectl get pv -n $NAMESPACE -o yaml > persistentvolumes.yaml
  kubectl get pvc -n $NAMESPACE -o yaml > persistentvolumeclaims.yaml
  kubectl get service -n $NAMESPACE -o yaml > services.yaml
  kubectl get deployment -n $NAMESPACE -o yaml > deployments.yaml
  kubectl get statefulset -n $NAMESPACE -o yaml > statefulsets.yaml
  ```

# Cleaning the workspace once all your test has finished
* Removing the namespace, this will delete all your resources within this namespace.
  ```helm delete airflow --namespace {namespace}```
* Removing the helm repo.
  ```helm repo remove apache-airflow```

#include "conf-infomap.h"

using namespace std;
using std::cout;
using std::cin;
using std::endl;

unsigned stou(char *s){
  return strtoul(s,(char **)NULL,10);
}

void partition(MTRand *R,Node ***node, GreedyBase *greedy, bool silent);
void repeated_partition(MTRand *R, Node ***node, GreedyBase *greedy, bool silent,int Ntrials);
void printTree(string s,multimap<double,treeNode,greater<double> >::iterator it_tM,ofstream *outfile);
void printSignificantTree(string s,multimap<double,treeNode,greater<double> >::iterator it_tM,ofstream *outfile,vector<bool> &significantVec);
void findConfCore(multimap<double,treeNode,greater<double> > &treeMap,vector<vector<int > > &bootClusters,vector<bool> &significantVec,double conf,MTRand *R);
void findConfModules(multimap<double,treeNode,greater<double> > &treeMap,vector<vector<int > > &bootClusters,vector<bool> &significantVec,vector<pair<int,int> > &mergers,double conf);

// Call: trade <seed> <Ntries>
int main(int argc,char *argv[]){
  
  if( argc < 3 ){
    cout << "Call: ./conf-infomap <seed> <network.net> <# attempts/network [10]> <# bootstrap resamples [100]> <conf level [0.90]>" << endl;
    exit(-1);
  }

  MTRand *R = new MTRand(stou(argv[1])); // Set random seed
  StochasticLib1 sto(atoi(argv[1]));
  string networkFile = string(argv[2]);
  int Ntrials = 10;
  if(argc > 3)
    Ntrials = atoi(argv[3]); // Set number of partition attempts
  int Nbootstraps = 100;
  if(argc > 4)
    Nbootstraps = atoi(argv[4]); // Number of network resamples
  double conf = 0.90;
  if(argc > 5)
    conf = atof(argv[5]); // Confidence level. 
  
  cout << "Running significance analysis on " << networkFile << " with " << Nbootstraps << " bootstrap networks (based on best clustering from " << Ntrials << " attempts per network) and confidence level " << conf << "." << endl; 
  string networkName(networkFile.begin(),networkFile.begin() + networkFile.find_last_of("."));
  
  Network network(networkFile);
  loadPajekNet(network);
  
  int Nnode = network.Nnode;
  
  /////////// Partition bootstrap networks /////////////////////
  
  vector<vector<int > > bootClusters = vector<vector<int > >(Nbootstraps,vector<int>(Nnode));
  
  for(int bootstrap = 0;bootstrap < Nbootstraps ; bootstrap++){
    cout << endl << "Bootstrap " << bootstrap+1 << "/" << Nbootstraps << endl;

    double totalDegree = 0.0;
    Node **node = new Node*[Nnode];
    for(int i=0;i<Nnode;i++){
      node[i] = new Node(i);
    }
    
    int NselfLinks = 0;
    for(map<int,map<int,double> >::iterator fromLink_it = network.Links.begin(); fromLink_it != network.Links.end(); fromLink_it++){
      for(map<int,double>::iterator toLink_it = fromLink_it->second.begin(); toLink_it != fromLink_it->second.end(); toLink_it++){
        
        int from = fromLink_it->first;
        int to = toLink_it->first;
        double weight = toLink_it->second;
        weight = 1.0*sto.Normal(weight,sqrt(weight)); // Generate normal random number
        if(weight > 0.0){
          if(from == to){
            NselfLinks++;
          }
          else{
            node[from]->links.push_back(make_pair(to,weight));
            node[to]->links.push_back(make_pair(from,weight));
            node[from]->degree += weight;
            node[to]->degree += weight;
            totalDegree += 2*weight;
          }
        }
      }
    }
    
    // Initiation
    GreedyBase* greedy;
    greedy = new Greedy(R,Nnode,totalDegree,node);
    greedy->initiate();
    
    double uncompressedCodeLength = -greedy->nodeDegree_log_nodeDegree;
    
    cout << "Now partition the network:" << endl;
    repeated_partition(R,&node,greedy,false,Ntrials);
    int Nmod = greedy->Nnode;
    cout << "Done! Code length " << greedy->codeLength << " in " << Nmod << " modules." << endl;
    cout << "Compressed by " << 100.0*(1.0-greedy->codeLength/uncompressedCodeLength) << " percent." << endl;

    for(int i=0;i<Nmod;i++){
      int Nmem = node[i]->members.size();
      for(int j=0;j<Nmem;j++){
        bootClusters[bootstrap][node[i]->members[j]] = i; 
      }
    }
    
    for(int i=0;i<greedy->Nnode;i++){
      delete node[i];
    }
    delete [] node;
    delete greedy;
    
  }
  
  /////////// Partition network /////////////////////
  
  double totalDegree = 0.0;
  vector<double> degree(Nnode);
  Node **node = new Node*[Nnode];
  for(int i=0;i<Nnode;i++){
    node[i] = new Node(i);
    degree[i] = 0.0;
  }
  
  int NselfLinks = 0;
  for(map<int,map<int,double> >::iterator fromLink_it = network.Links.begin(); fromLink_it != network.Links.end(); fromLink_it++){
    for(map<int,double>::iterator toLink_it = fromLink_it->second.begin(); toLink_it != fromLink_it->second.end(); toLink_it++){
      
      int from = fromLink_it->first;
      int to = toLink_it->first;
      double weight = toLink_it->second;
      if(weight > 0.0){
        if(from == to){
          NselfLinks++;
        }
        else{
          node[from]->links.push_back(make_pair(to,weight));
          node[to]->links.push_back(make_pair(from,weight));
          node[from]->degree += weight;
          node[to]->degree += weight;
          totalDegree += 2*weight;
          degree[from] += weight;
          degree[to] += weight;
        }
      }
    }
  }
  if(NselfLinks > 0)
    cout << ", ignoring " <<  NselfLinks << " self link(s)." << endl;
  else
    cout << ")" << endl;
  
  //  //Swap maps to free memory
  //  for(map<int,map<int,double> >::iterator it = Links.begin(); it != Links.end(); it++)
  //    map<int,double>().swap(it->second);
  //  map<int,map<int,double> >().swap(Links);
  
  // Initiation
  GreedyBase* greedy;
  greedy = new Greedy(R,Nnode,totalDegree,node);
  greedy->initiate();
  
  double uncompressedCodeLength = -greedy->nodeDegree_log_nodeDegree;
  
  cout << "Now partition the network:" << endl;
  repeated_partition(R,&node,greedy,false,Ntrials);
  int Nmod = greedy->Nnode;
  cout << "Done! Code length " << greedy->codeLength << " in " << Nmod << " modules." << endl;
  cout << "Compressed by " << 100.0*(1.0-greedy->codeLength/uncompressedCodeLength) << " percent." << endl;
  
  // Order modules by size
  multimap<double,treeNode,greater<double> > treeMap;
  multimap<double,treeNode,greater<double> >::iterator it_tM;
  for(int i=0;i<greedy->Nnode;i++){
    
    int Nmembers = node[i]->members.size();
    treeNode tmp_tN;
    it_tM = treeMap.insert(make_pair(node[i]->degree/totalDegree,tmp_tN));
    for(int j=0;j<Nmembers;j++)
      it_tM->second.members.insert(make_pair(degree[node[i]->members[j]]/totalDegree,make_pair(node[i]->members[j],network.nodeNames[node[i]->members[j]]))); 
    
  }
  
  // Order links by size
  multimap<double,pair<int,int>,greater<double> > sortedLinks;
  for(int i=0;i<Nmod;i++){
    int Nlinks = node[i]->links.size();
    for(int j=0;j<Nlinks;j++){
      if(i <= node[i]->links[j].first)
        sortedLinks.insert(make_pair(node[i]->links[j].second/totalDegree,make_pair(i+1,node[i]->links[j].first+1)));
    }
  }
  
  // Print map in .map format for the Map Generator at www.mapequation.org
  
  ofstream outfile;
  ostringstream oss;
  oss << networkName << ".map";
  outfile.open(oss.str().c_str());
  outfile << "# modules: " << Nmod << endl;
  outfile << "# modulelinks: " << sortedLinks.size() << endl;
  outfile << "# nodes: " << Nnode << endl;
  outfile << "# links: " << network.Nlinks << endl;
  outfile << "# codelength: " << greedy->codeLength << endl;
  outfile << "*Undirected" << endl;
  outfile << "*Modules " << Nmod << endl;
  int k = 0;
  for(multimap<double,treeNode,greater<double> >::iterator it = treeMap.begin(); it != treeMap.end(); it++){
    outfile << k+1 << " \"" << it->second.members.begin()->second.second << ",...\" " << it->first << " " << node[k]->exit/totalDegree << endl;
    k++;
  }
  outfile << "*Nodes " << Nnode << endl;
  k = 1;
  for(multimap<double,treeNode,greater<double> >::iterator it = treeMap.begin(); it != treeMap.end(); it++){
    string s;
    s.append(to_string(k));
    s.append(":");
    printTree(s,it,&outfile);
    k++;
  }
  outfile << "*Links " << sortedLinks.size() << endl;
  for(multimap<double,pair<int,int>,greater<double> >::iterator it = sortedLinks.begin();it != sortedLinks.end();it++)   
    outfile << it->second.first << " " << it->second.second << " " << 1.0*it->first << endl;
  outfile.close();
    
  /////////// Confidence analysis /////////////////////
  
  cout << endl << "Confidence analysis" << endl;
  
  vector<bool> significantVec = vector<bool>(Nnode);
  findConfCore(treeMap,bootClusters,significantVec,conf,R);
  vector<pair<int,int> > mergers;
  findConfModules(treeMap,bootClusters,significantVec,mergers,conf);
  
  // Print significance map in .smap format for the Map Generator at www.mapequation.org
  
  oss.str("");
  oss << networkName << ".smap";
  outfile.open(oss.str().c_str());
  outfile << "# modules: " << Nmod << endl;
  outfile << "# modulelinks: " << sortedLinks.size() << endl;
  outfile << "# nodes: " << Nnode << endl;
  outfile << "# links: " << network.Nlinks << endl;
  outfile << "# codelength: " << greedy->codeLength << endl;
  outfile << "*Undirected" << endl;
  outfile << "*Modules " << Nmod << endl;
  k = 0;
  for(multimap<double,treeNode,greater<double> >::iterator it = treeMap.begin(); it != treeMap.end(); it++){
    outfile << k+1 << " \"" << it->second.members.begin()->second.second << ",...\" " << it->first << " " << node[k]->exit/totalDegree << endl;
    k++;
  }
  outfile << "*Insignificants " << mergers.size() << endl;
  for(vector<pair<int,int> >::iterator it = mergers.begin(); it != mergers.end(); it++)
    outfile << it->first+1 << ">" << it->second+1 << endl;
  outfile << "*Nodes " << Nnode << endl;
  k = 1;
  for(multimap<double,treeNode,greater<double> >::iterator it = treeMap.begin(); it != treeMap.end(); it++){
    string s;
    s.append(to_string(k));
    printSignificantTree(s,it,&outfile,significantVec);
    k++;
  }
  outfile << "*Links " << sortedLinks.size() << endl;
  for(multimap<double,pair<int,int>,greater<double> >::iterator it = sortedLinks.begin();it != sortedLinks.end();it++)   
    outfile << it->second.first << " " << it->second.second << " " << 1.0*it->first << endl;
  outfile.close();
  
  for(int i=0;i<greedy->Nnode;i++){
    delete node[i];
  }
  delete [] node;
  delete greedy;
  delete R;
  
}

void partition(MTRand *R,Node ***node, GreedyBase *greedy, bool silent){
  
  int Nnode = greedy->Nnode;
  Node **cpy_node = new Node*[Nnode];
  for(int i=0;i<Nnode;i++){
    cpy_node[i] = new Node();
    cpyNode(cpy_node[i],(*node)[i]);
  }
  
  int iteration = 0;
  double outer_oldCodeLength;
  do{
    outer_oldCodeLength = greedy->codeLength;
    
    if((iteration > 0) && (iteration % 2 == 0) && (greedy->Nnode > 1)){  // Partition the partition
      
      
      if(!silent)
        cout << "Iteration " << iteration+1 << ", moving " << flush;
      
      Node **rpt_node = new Node*[Nnode];
      for(int i=0;i<Nnode;i++){
        rpt_node[i] = new Node();
        cpyNode(rpt_node[i],cpy_node[i]);
      }
      vector<int> subMoveTo(Nnode);
      vector<int> moveTo(Nnode);
      int subModIndex = 0;
      
      for(int i=0;i<greedy->Nnode;i++){
        
        int sub_Nnode = (*node)[i]->members.size();
        
        if(sub_Nnode > 1){
          
          Node **sub_node = new Node*[sub_Nnode]; 
          set<int> sub_mem;
          for(int j=0;j<sub_Nnode;j++)
            sub_mem.insert((*node)[i]->members[j]);
          set<int>::iterator it_mem = sub_mem.begin();
          int *sub_renumber = new int[Nnode];
          int *sub_rev_renumber = new int[sub_Nnode];
          double totalDegree = 0.0;
          for(int j=0;j<sub_Nnode;j++){
            
            //    fprintf(stderr,"%d %d\n",j,(*it_mem));
            int orig_nr = (*it_mem);
            int orig_Nlinks = cpy_node[orig_nr]->links.size(); // ERROR HERE
            sub_renumber[orig_nr] = j;
            sub_rev_renumber[j] = orig_nr;
            sub_node[j] = new Node(j);
            for(int k=0;k<orig_Nlinks;k++){
              int orig_link = cpy_node[orig_nr]->links[k].first;
              int orig_link_newnr = sub_renumber[orig_link];
              double orig_weight = cpy_node[orig_nr]->links[k].second;
              if(orig_link < orig_nr){
                if(sub_mem.find(orig_link) != sub_mem.end()){
                  sub_node[j]->links.push_back(make_pair(orig_link_newnr,orig_weight));
                  sub_node[orig_link_newnr]->links.push_back(make_pair(j,orig_weight));
                  totalDegree += 2.0*orig_weight;
                }
              }
            }
            it_mem++;
          }
          
          GreedyBase* sub_greedy;
          sub_greedy = new Greedy(R,sub_Nnode,totalDegree,sub_node);
          sub_greedy->initiate();
          partition(R,&sub_node,sub_greedy,true);
          for(int j=0;j<sub_greedy->Nnode;j++){
            int Nmembers = sub_node[j]->members.size();
            for(int k=0;k<Nmembers;k++){
              subMoveTo[sub_rev_renumber[sub_node[j]->members[k]]] = subModIndex;
            }
            moveTo[subModIndex] = i;
            subModIndex++;
            delete sub_node[j];
          }
          
          delete [] sub_node;
          delete sub_greedy;
          delete [] sub_renumber;
          delete [] sub_rev_renumber;
          
        }
        else{
          
          subMoveTo[(*node)[i]->members[0]] = subModIndex;
          moveTo[subModIndex] = i;
          
          subModIndex++;
          
        }
      }
      
      for(int i=0;i<greedy->Nnode;i++)
        delete (*node)[i];
      delete [] (*node);
      
      greedy->Nnode = Nnode;
      greedy->Nmod = Nnode;
      greedy->node = rpt_node;
      greedy->initiate();
      greedy->determMove(subMoveTo);
      greedy->level(node,false); 
      greedy->determMove(moveTo);
      (*node) = rpt_node;
      
      outer_oldCodeLength = greedy->codeLength;
      
      if(!silent)
        cout << greedy->Nnode << " modules, looping " << flush;
      
    }
    else if(iteration > 0){
      
      if(!silent)
        cout << "Iteration " << iteration+1 << ", moving " << Nnode << " nodes, looping " << flush;
      
      
      Node **rpt_node = new Node*[Nnode];
      for(int i=0;i<Nnode;i++){
        rpt_node[i] = new Node();
        cpyNode(rpt_node[i],cpy_node[i]);
      }
      
      vector<int> moveTo(Nnode);
      for(int i=0;i<greedy->Nnode;i++){
        int Nmembers = (*node)[i]->members.size();
        for(int j=0;j<Nmembers;j++){
          moveTo[(*node)[i]->members[j]] = i;
        }
      }
      
      for(int i=0;i<greedy->Nnode;i++)
        delete (*node)[i];
      delete [] (*node);
      
      greedy->Nnode = Nnode;
      greedy->Nmod = Nnode;
      greedy->node = rpt_node;
      greedy->initiate();
      greedy->determMove(moveTo);
      
      (*node) = rpt_node;
    }
    else{
      
      if(!silent)
        cout << "Iteration " << iteration+1 << ", moving " << Nnode << " nodes, looping " << flush;
      
    }
    
    double oldCodeLength;
    do{
      oldCodeLength = greedy->codeLength;
      bool moved = true;
      int Nloops = 0;
      int count = 0;
      while(moved){
        moved = false;
        double inner_oldCodeLength = greedy->codeLength;
        greedy->move(moved);
        Nloops++;
        count++;
        if(fabs(inner_oldCodeLength-greedy->codeLength) < 1.0e-10)
          moved = false;
        
        if(count == 10){	  
          greedy->tune();
          count = 0;
        }
        // 	if(!silent){
        // 	  cerr << Nloops;
        // 	  int loopsize = to_string(Nloops).length();
        // 	  for(int i=0;i<loopsize;i++)
        // 	    cerr << "\b";
        // 	}
      }
      
      greedy->level(node,true);
      
      if(!silent)
        cout << Nloops << " " << flush;
      
    } while(oldCodeLength - greedy->codeLength >  1.0e-10);
    
    iteration++;
    if(!silent)
      cout << "times between mergings to code length " <<  greedy->codeLength << " in " << greedy->Nmod << " modules." << endl;
    
  } while(outer_oldCodeLength - greedy->codeLength > 1.0e-10);
  
  for(int i=0;i<Nnode;i++)
    delete cpy_node[i];
  delete [] cpy_node;
  
}

void repeated_partition(MTRand *R, Node ***node, GreedyBase *greedy, bool silent,int Ntrials){
  
  double shortestCodeLength = 1000.0;
  int Nnode = greedy->Nnode;
  vector<int> cluster(Nnode);
  
  for(int trial = 0; trial<Ntrials;trial++){
    
    if(!silent)
      cout << "Attempt " << trial+1 << "/" << Ntrials << endl;
    
    Node **cpy_node = new Node*[Nnode];
    for(int i=0;i<Nnode;i++){
      cpy_node[i] = new Node();
      cpyNode(cpy_node[i],(*node)[i]);
    }
    
    greedy->Nnode = Nnode;
    greedy->Nmod = Nnode;
    greedy->node = cpy_node;
    greedy->initiate();
    
    partition(R,&cpy_node,greedy,silent);
    
    if(greedy->codeLength < shortestCodeLength){
      
      shortestCodeLength = greedy->codeLength;
      
      // Store best partition
      for(int i=0;i<greedy->Nnode;i++){
        for(vector<int>::iterator mem = cpy_node[i]->members.begin(); mem != cpy_node[i]->members.end(); mem++){
          cluster[(*mem)] = i;
        }
      }
    }
    
    for(int i=0;i<greedy->Nnode;i++){
      delete cpy_node[i];
    }
    delete [] cpy_node;
    
  }
  
  // Commit best partition
  greedy->Nnode = Nnode;
  greedy->Nmod = Nnode;
  greedy->node = (*node);
  greedy->initiate();
  greedy->determMove(cluster);
  greedy->level(node,true);
  
}

void printTree(string s,multimap<double,treeNode,greater<double> >::iterator it_tM,ofstream *outfile){
  
  multimap<double,treeNode,greater<double> >::iterator it;
  if(it_tM->second.nextLevel.size() > 0){
    int i=1;
    for(it = it_tM->second.nextLevel.begin(); it != it_tM->second.nextLevel.end(); it++){
      string cpy_s(s + to_string(i) + ":");
      printTree(cpy_s,it,outfile);
      i++;
    }
  }
  else{
    int i = 1;
    for(multimap<double,pair<int,string>,greater<double> >::iterator mem = it_tM->second.members.begin(); mem != it_tM->second.members.end(); mem++){
        string cpy_s(s + to_string(i) + " \"" + mem->second.second + "\" " + to_string(mem->first));
        (*outfile) << cpy_s << endl;
      i++;
    } 
  }  
}

void printSignificantTree(string s,multimap<double,treeNode,greater<double> >::iterator it_tM,ofstream *outfile,vector<bool> &significantVec){
  
  multimap<double,treeNode,greater<double> >::iterator it;
  if(it_tM->second.nextLevel.size() > 0){
    int i=1;
    for(it = it_tM->second.nextLevel.begin(); it != it_tM->second.nextLevel.end(); it++){
      string cpy_s(s + to_string(i));
      printSignificantTree(cpy_s,it,outfile,significantVec);
      i++;
    }
  }
  else{
    int i = 1;
    for(multimap<double,pair<int,string>,greater<double> >::iterator mem = it_tM->second.members.begin(); mem != it_tM->second.members.end(); mem++){
      string cpy_s(s + (significantVec[mem->second.first] == true ? (":") : (";") ) + to_string(i) + " \"" + mem->second.second + "\" " + to_string(mem->first));
      (*outfile) << cpy_s << endl;
      i++;
    } 
  }  
}

void findConfCore(multimap<double,treeNode,greater<double> > &treeMap,vector<vector<int > > &bootClusters,vector<bool> &significantVec,double conf,MTRand *R){
  
  int Nboots = bootClusters.size();
  int Nremove = static_cast<int>((1.0-conf)*Nboots+0.5);
  
  int Nnode = bootClusters[0].size();
  vector<double> size = vector<double>(Nnode);
  
  int M = treeMap.size();
  vector<double> moduleSize = vector<double>(M);
  
  vector<vector<int> > modSortMembers = vector<vector<int> >(M);
  int i = 0;
  
  for(multimap<double,treeNode>::iterator it = treeMap.begin(); it != treeMap.end(); it++){
    int Nmem = it->second.members.size();
    modSortMembers[i] = vector<int>(Nmem);
    int j=0;
    for(multimap<double,pair<int,string>,greater<double> >::iterator it2 = it->second.members.begin(); it2 != it->second.members.end(); it2++){
      int mem = it2->second.first;
      modSortMembers[i][j] = mem;
      size[mem] = 1.0*it2->first;
      moduleSize[i] += size[mem];
      j++;
    }
    i++;
  }
  
  
  cout << "MCMC to maximize confidence size of " << endl;
  for(int i=0;i<M;i++){
    
    cout << "module " << i+1 << ": " << flush;
    
    int N = modSortMembers[i].size();
    vector<bool> confState = vector<bool>(N);
    vector<bool> maxConfState = vector<bool>(N);
    double maxScore = -1.0;
    
    double confSize = 0.0;
    int confN = 0;
    double maxConfSize = 0.0;
    int maxConfN = 0;
    double score = 0.0;
    int penalty = 0;
    
    double pW = 10.0*moduleSize[i];
    
    if(N != 1){
      
      int maxModNr = 0;
      for(int j=0;j<Nboots;j++)
        for(int k=0;k<N;k++)
          if(bootClusters[j][modSortMembers[i][k]] > maxModNr )
            maxModNr = bootClusters[j][modSortMembers[i][k]];
      maxModNr++;
      
      // Initiate weights of module assignments
      
      // Keep track of the size order of modules
      vector<multimap<double,int,greater<double> > > sortModSizes = vector<multimap<double,int,greater<double> > >(Nboots);
      // Keep track of which modules that are included
      vector<vector<pair<int,multimap<double,int,greater<double> >::iterator > > > mapModSizes = vector<vector<pair<int,multimap<double,int,greater<double> >::iterator > > >(Nboots);
      for(int j=0;j<Nboots;j++){
        mapModSizes[j] = vector<pair<int,multimap<double,int,greater<double> >::iterator > >(maxModNr);
        for(int k=0;k<maxModNr;k++){
          mapModSizes[j][k].first = 0;
        }
      }
      
      // Randomized start
      for(int j=0;j<N;j++){
        if(R->randInt() << 31){
          confState[j] = true;
          confSize += size[modSortMembers[i][j]];
          confN++;
          
          for(int k=0;k<Nboots;k++){
            
            int modNr = bootClusters[k][modSortMembers[i][j]];
            if(mapModSizes[k][modNr].first == 0){
              double newSize = size[modSortMembers[i][j]];
              multimap<double,int,greater<double> >::iterator it = sortModSizes[k].insert(make_pair(newSize,modNr));
              mapModSizes[k][modNr].second = it;
              mapModSizes[k][modNr].first++;
            }
            else{
              double newSize = size[modSortMembers[i][j]] + mapModSizes[k][modNr].second->first;
              multimap<double,int,greater<double> >::iterator it = sortModSizes[k].insert(mapModSizes[k][modNr].second,make_pair(newSize,modNr));
              sortModSizes[k].erase(mapModSizes[k][modNr].second);
              mapModSizes[k][modNr].second = it;
              mapModSizes[k][modNr].first++;
            }
            
          }
        }
        else
          confState[j] = false;
      }
      
      multimap<double,pair<int,int> > scoreRank;
      score = 0.0;
      // Calculate penalty
      for(int j=0;j<Nboots;j++){
				double tmpScore = 0.0;
				int tmpPenalty = 0;
				if(!sortModSizes[j].empty()){
        		int modNr = sortModSizes[j].begin()->second; 
         		tmpScore = sortModSizes[j].begin()->first;
						tmpPenalty = confN - mapModSizes[j][modNr].first; //penalty is the number of nodes not in biggest field
				}
        scoreRank.insert(make_pair(tmpScore-pW*tmpPenalty,make_pair(tmpPenalty,j)));
        score += tmpScore;
        penalty += tmpPenalty;
      }
      
      // Remove worst results
      multimap<double,pair<int,int> >::iterator it = scoreRank.begin();
      for(int j=0;j<Nremove;j++){
        int bootNr = it->second.second;
				double tmpScore = 0.0;
				int tmpPenalty = 0;
				if(!sortModSizes[bootNr].empty()){
        	tmpScore = sortModSizes[bootNr].begin()->first;
        	tmpPenalty = it->second.first;
				}
        score -= tmpScore;
        penalty -= tmpPenalty;
        it++;
      }
      
      
      //Monte Carlo to maximize confident size
      int Niter = static_cast<int>(pow(1.0*N,1.0));
      if(Niter < 100)
        Niter = 100;
      int attempts = 0;
      int switches = 0;
      bool search = true;
      while(search){
        
        double T = 1.0;
        
        do{
          
          attempts = 0;
          switches = 0;
          for(int j=0;j<Niter;j++){
            
            multimap<double,pair<int,int> >().swap(scoreRank);
            double newConfSize = confSize;
            int newConfN = confN;
            double newScore = 0.0;
            int newPenalty = 0;
            
            int flip = R->randInt(N-1);
            int nodeNr = modSortMembers[i][flip];
            
            if(confState[flip]){ // Remove one node from confident subset
              newConfSize -= size[nodeNr];
              newConfN--;
              for(int k=0;k<Nboots;k++){
                int modNr = bootClusters[k][nodeNr];
                double tmpScore = sortModSizes[k].begin()->first;
                int tmpPenalty = newConfN - mapModSizes[k][sortModSizes[k].begin()->second].first;
                if(mapModSizes[k][modNr].second == sortModSizes[k].begin()){
                  tmpScore -= size[nodeNr];
                  tmpPenalty = newConfN - (mapModSizes[k][modNr].first-1);
                  if(sortModSizes[k].size() > 1){ 
                    multimap<double,int,greater<double> >::iterator it = sortModSizes[k].begin();
                    it++;
                    if(it->first > tmpScore){ // Check if second in ranking is larger
                      tmpScore = it->first;
                      tmpPenalty = newConfN - mapModSizes[k][it->second].first;
                    }
                  }
                }
                scoreRank.insert(make_pair(tmpScore-pW*tmpPenalty,make_pair(tmpPenalty,k)));
                newScore += tmpScore;
                newPenalty += tmpPenalty;
              }
            }
            else{ // Add one node to confident subset
              newConfSize += size[nodeNr];
              newConfN++;
              for(int k=0;k<Nboots;k++){
                
                int modNr = bootClusters[k][nodeNr];
                double tmpScore = 0.0;
                int tmpPenalty = 0;
                if(sortModSizes[k].empty()){ // No nodes in confident subset
                  tmpScore = size[nodeNr];
                  tmpPenalty = 0;
                }
                else{
                  
                  if(mapModSizes[k][modNr].first == 0){ // First confident node in module
                    if(size[nodeNr] > sortModSizes[k].begin()->first){
                      tmpScore = size[nodeNr];
                      tmpPenalty = newConfN - 1;
                    }
                    else{
                      tmpScore = sortModSizes[k].begin()->first;
                      tmpPenalty = newConfN - mapModSizes[k][sortModSizes[k].begin()->second].first;
                    }
                  }
                  else{ // Not first confident node in module
                    
                    if(mapModSizes[k][modNr].second == sortModSizes[k].begin()){
                      tmpScore = sortModSizes[k].begin()->first + size[nodeNr];
                      tmpPenalty = newConfN - (mapModSizes[k][sortModSizes[k].begin()->second].first+1);
                    }
                    else{
                      
                      if(mapModSizes[k][modNr].second->first + size[nodeNr] > sortModSizes[k].begin()->first){
                        tmpScore = mapModSizes[k][modNr].second->first + size[nodeNr];
                        tmpPenalty = newConfN - (mapModSizes[k][modNr].first+1);
                      }
                      else{
                        tmpScore = sortModSizes[k].begin()->first;
                        tmpPenalty = newConfN - mapModSizes[k][sortModSizes[k].begin()->second].first;
                      }
                      
                    }
                    
                  }
                }
                
                scoreRank.insert(make_pair(tmpScore-pW*tmpPenalty,make_pair(tmpPenalty,k)));
                newScore += tmpScore;
                newPenalty += tmpPenalty;
              }
            }
            
            // Remove worst results
            multimap<double,pair<int,int> >::iterator it = scoreRank.begin();
            for(int j=0;j<Nremove;j++){
              int bootNr = it->second.second;
              if(!sortModSizes[bootNr].empty()){
                double tmpScore = sortModSizes[bootNr].begin()->first;
                int tmpPenalty = it->second.first;
                newScore -= tmpScore;
                newPenalty -= tmpPenalty;
              }
               
              it++;
            }
            
            if(exp(((newScore-pW*newPenalty)-(score-pW*penalty))/T) > R->rand()){
              
              // Update data structures
              if(confState[flip]){ // Remove one node from confident subset
                
                for(int k=0;k<Nboots;k++){
                  int modNr = bootClusters[k][nodeNr];
                  mapModSizes[k][modNr].first--;
                  if(mapModSizes[k][modNr].first == 0){ // Remove last confident node from module
                    sortModSizes[k].erase(mapModSizes[k][modNr].second);
                  }
                  else{
                    double newSize = mapModSizes[k][modNr].second->first - size[nodeNr];
                    multimap<double,int,greater<double> >::iterator it = sortModSizes[k].insert(mapModSizes[k][modNr].second,make_pair(newSize,modNr));
                    sortModSizes[k].erase(mapModSizes[k][modNr].second);
                    mapModSizes[k][modNr].second = it;
                  }
                  
                }
              }
              else{ // Add one node from confident subset
                
                for(int k=0;k<Nboots;k++){
                  
                  int modNr = bootClusters[k][nodeNr];
                  if(mapModSizes[k][modNr].first == 0){
                    double newSize = size[nodeNr];
                    multimap<double,int,greater<double> >::iterator it = sortModSizes[k].insert(make_pair(newSize,modNr));
                    mapModSizes[k][modNr].second = it;
                    mapModSizes[k][modNr].first++;
                  }
                  else{
                    double newSize = size[nodeNr] + mapModSizes[k][modNr].second->first;
                    multimap<double,int,greater<double> >::iterator it = sortModSizes[k].insert(mapModSizes[k][modNr].second,make_pair(newSize,modNr));
                    sortModSizes[k].erase(mapModSizes[k][modNr].second);
                    mapModSizes[k][modNr].second = it;
                    mapModSizes[k][modNr].first++;
                  }
                  
                }
                
              }
              
              confSize = newConfSize;
              confN = newConfN;
              confState[flip] = !confState[flip];
              penalty = newPenalty;
              score = newScore;
              switches++;
            }
            attempts++;
            
            if(penalty == 0 && score > maxScore){
              for(int k=0;k<N;k++)
                maxConfState[k] = confState[k];
              maxScore = score;
              maxConfSize = confSize;
              maxConfN = confN;
            }
            
          }
          T *= 0.99;
          //cout << T << " " <<  1.0*switches/attempts << " " << score << " " << penalty << "    " << confSize << " " << confN << endl;
        } while(switches > 0);
        
        if(maxScore > 0.0)
          search = false;
        
      }
      
    }
    else{
      maxConfState[0] = true;
      maxConfSize = moduleSize[i];
      maxConfN = 1;
    }
    
    
    cout << maxConfN << "/" << N << " confident nodes and " << maxConfSize << "/" << moduleSize[i] << " (" << 100*maxConfSize/moduleSize[i] << " percent) of the flow." << endl;
    
    for(int j=0;j<N;j++)
      significantVec[modSortMembers[i][j]] = maxConfState[j];
    
  }
  
//  i = 0;
//  for(multimap<double,treeNode>::reverse_iterator it = treeMap.rbegin(); it != treeMap.rend(); it++){
//    int j=0;
//    for(multimap<double,treeNode>::reverse_iterator it2 = it->second.nextLevel.rbegin(); it2 != it->second.nextLevel.rend(); it2++){
//      it2->second.significant = significantVec[modSortMembers[i][j]];
//      j++;
//    }
//    i++;
//  }
  
}

void findConfModules(multimap<double,treeNode,greater<double> > &treeMap,vector<vector<int > > &bootClusters,vector<bool> &significantVec,vector<pair<int,int> > &mergers,double conf){
  
  
  int M = treeMap.size();
  int N = bootClusters[0].size();
  int Nboots = bootClusters.size();
  
  // Calculate total size of confident journals in field
  vector<vector<int> > significantNodes = vector<vector<int> >(N);
  vector<double> confFieldSize = vector<double>(M,0.0);
  vector<multimap<int,pair<int,vector<int> >,greater<int> > > coExist = vector<multimap<int,pair<int,vector<int> >,greater<int> > >(M);

  
  int clusterNr = 0;
  for(multimap<double,treeNode,greater<double> >::iterator it = treeMap.begin();  it != treeMap.end(); it++){
    for(multimap<double,pair<int,string>,greater<double> >::iterator it2 = it->second.members.begin(); it2 != it->second.members.end(); it2++){
      if(significantVec[it2->second.first])
        significantNodes[clusterNr].push_back(it2->second.first);
    }
    clusterNr++;
  }
  
  vector<vector<int> > coexistCount = vector<vector<int> >(M);
  for(int i=0;i<M;i++)
    coexistCount[i] = vector<int>(Nboots,0);
  
  cout << endl << "Now calculate number of times two modules are clustered together" << endl;
  int i=0;
  for(multimap<double,treeNode,greater<double> >::iterator it1 = treeMap.begin();  it1 != treeMap.end(); it1++){ // i
    int j=i;
    for(multimap<double,treeNode,greater<double> >::iterator it2 = it1;  it2 != treeMap.end(); it2++){ // j
            
      if(it1 != it2){
        
        int coEx = 0;
        for(int k=0;k<Nboots;k++){
          int modNr = bootClusters[k][significantNodes[j][0]];
          bool joined = true;
          int iNnode = significantNodes[i].size();
          int jNnode = significantNodes[j].size();
          
          for(int l=0;l<jNnode;l++){
            if(bootClusters[k][significantNodes[j][l]] != modNr){
              joined = false;
              break;
            }
          }
          
          if(joined){
            for(int l=0;l<iNnode;l++){
              if(bootClusters[k][significantNodes[i][l]] != modNr){
                joined = false;
                break;
              }
            }
          }
          
          if(joined){
            coEx++;
            coexistCount[i][k]++;
            coexistCount[j][k]++;
            
            multimap<int,pair<int,vector<int> >,greater<int> >::iterator it = coExist[i].find(j);
            if(it != coExist[i].end()){
              it->second.first++;
              it->second.second.push_back(k);
            }
            else{
              vector<int> tmp;
              tmp.push_back(k);
              coExist[i].insert(make_pair(j,make_pair(1,tmp)));
            }
            it = coExist[j].find(i);
            if(it != coExist[j].end()){
              it->second.first++;
              it->second.second.push_back(k);
            }
            else{
              vector<int> tmp;
              tmp.push_back(k);
              it = coExist[j].insert(make_pair(i,make_pair(1,tmp)));
            }
          }
          
        }
        
        
      }
      
      j++;
    }
    
    // Re-sort co-exist strcuture
    multimap<int,pair<int,vector<int> >,greater<int> > tmp = coExist[i];
    multimap<int,pair<int,vector<int> >,greater<int> >().swap(coExist[i]);
    for(multimap<int,pair<int,vector<int> >,greater<int> >::iterator it = tmp.begin(); it != tmp.end(); it++){
      coExist[i].insert(make_pair(it->second.first,make_pair(it->first,it->second.second)));
    }
    
    i++;
    
  }
  
  vector<int> mergeVec = vector<int>(M);
  i=0;
  for(multimap<double,treeNode,greater<double> >::iterator it1 = treeMap.begin();  it1 != treeMap.end(); it1++){
    int singleN = 0;
    for(int k=0;k<Nboots;k++)
      if(coexistCount[i][k] == 0)
        singleN++;
    cout << "Module " << i+1 << " is standalone " << singleN << "/" << Nboots << " times";
    if(singleN == Nboots){
      cout << "." << endl;
    }
    else{
      cout << " and clustered together with: ";
      for(multimap<int,pair<int,vector<int> >,greater<int> >::iterator it2 = coExist[i].begin(); it2 != coExist[i].end(); it2++)
        cout << it2->second.first+1 << " (" << it2->first << "), ";
      cout << endl;
    }
    i++;
  }
  
  // Find merges
  for(int i=M-1;i>=0;i--){
    
    bool searchMerge = true;
    mergeVec[i] = i;
    while(searchMerge){
      int singleN = 0;
      for(int k=0;k<Nboots;k++)
        if(coexistCount[i][k] == 0)
          singleN++;
      if(1.0*singleN/Nboots < conf){
        int mergeWith = coExist[i].begin()->second.first;
        
        for(int j=0;j<coExist[i].begin()->first;j++){
          coexistCount[i][coExist[i].begin()->second.second[j]]--;
          coexistCount[mergeWith][coExist[i].begin()->second.second[j]]--;
        }
        coExist[i].erase(coExist[i].begin());
        
        for(multimap<int,pair<int,vector<int> >,greater<int> >::iterator it = coExist[mergeWith].begin(); it != coExist[mergeWith].end(); it++){
          if(it->second.first == i){
            coExist[mergeWith].erase(it);
            break;
          }
          
        }
        
        if(mergeWith < i){
          mergeVec[i] = mergeWith;
          mergers.push_back(make_pair(i,mergeWith));
          searchMerge = false;
        }
        
      }
      else{
        searchMerge = false;
      }
    }
  }

  if(mergers.size() > 0){
    cout << endl << "Module associations of modules that are not significantly standalone:" << endl;
    
    for(vector<pair<int,int> >::iterator it = mergers.begin(); it != mergers.end(); it++)
      cout << it->first+1 << " -> " << it->second+1 << endl;
  }
  else{
    cout << "All modules are significantly standalone." << endl;
  }
  
}



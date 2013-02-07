#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>
#include <sstream>
#include <fstream>
#include <iomanip>
#include "MersenneTwister.h"
#include "GreedyBase.h" 
#include "Greedy.h" 
#include "Node.h"
#include "stocc.h"
using namespace std;

unsigned stou(char *s);

class Network{
  
public:
  
  Network(string netname);
  string name;
  int Nnode;
  int Nlinks;
  vector<string> nodeNames;
  map<int,map<int,double> > Links;
  
};

Network::Network(string netname){
  name = netname;
}

class treeNode{
 public:
  multimap<double,pair<int,string>,greater<double> > members;
  multimap<double,treeNode, greater<double> > nextLevel;
};

template <class T>
inline std::string to_string (const T& t){
  std::stringstream ss;
  ss << t;
  return ss.str();
}


void cpyNode(Node *newNode,Node *oldNode){
  
  newNode->index = oldNode->index;
  newNode->exit = oldNode->exit;
  newNode->degree = oldNode->degree;

  int Nmembers = oldNode->members.size();
  newNode->members = vector<int>(Nmembers);
  for(int i=0;i<Nmembers;i++)
    newNode->members[i] = oldNode->members[i];
  
  int Nlinks = oldNode->links.size();
  newNode->links = vector<pair<int,double> >(Nlinks);
  for(int i=0;i<Nlinks;i++){
    newNode->links[i].first = oldNode->links[i].first;
    newNode->links[i].second = oldNode->links[i].second;
  }

}

void loadPajekNet(Network &network){
  
  string line;
  string buf;
  
  /* Read network in Pajek format with nodes ordered 1, 2, 3, ..., N,            */
  /* each undirected link occurring only once, and link weights > 0.             */
  /* (if a link is defined more than once, weights are aggregated)               */   
  /* For more information, see http://vlado.fmf.uni-lj.si/pub/networks/pajek/.   */
  /* Example network with three nodes and                                        */
  /* three undirected weighted links:                                            */
  /* *Vertices 3                                                                 */
  /* 1 "Name of first node"                                                      */
  /* 2 "Name of second node"                                                     */
  /* 3 "Name of third node"                                                      */
  /* *Edges 3                                                                    */
  /* 1 2 1.0                                                                     */
  /* 1 3 3.3                                                                     */
  /* 2 3 2.2                                                                   */
  
  cout << "Reading network " << network.name << "..." << flush;
  ifstream net(network.name.c_str());
  network.Nnode = 0;
  istringstream ss;
  while(network.Nnode == 0){ 
    if(getline(net,line) == NULL){
      cout << "the network file is not in Pajek format...exiting" << endl;
      exit(-1);
    }
    else{
      ss.clear();
      ss.str(line);
      ss >> buf;
      if(buf == "*Vertices" || buf == "*vertices" || buf == "*VERTICES"){
        ss >> buf;
        network.Nnode = atoi(buf.c_str());
      }
      else{
        cout << "the network file is not in Pajek format...exiting" << endl;
        exit(-1);
      }
    }
  }
  
  network.nodeNames = vector<string>(network.Nnode);
  
  // Read node names, assuming order 1, 2, 3, ...
  for(int i=0;i<network.Nnode;i++){
    getline(net,line);
    int nameStart = line.find_first_of("\"");
    int nameEnd = line.find_last_of("\"");
    if(nameStart < nameEnd){
      network.nodeNames[i] =  string(line.begin() + nameStart + 1,line.begin() + nameEnd);
      line = string(line.begin() + nameEnd + 1, line.end());
      ss.clear();
      ss.str(line);
    }
    else{
      ss.clear();
      ss.str(line);
      ss >> buf; 
      ss >> network.nodeNames[i];
    }
    
  }
  
  // Read the number of links in the network
  getline(net,line);
  ss.clear();
  ss.str(line);
  ss >> buf;
  
  if(buf != "*Edges" && buf != "*edges" && buf != "*Arcs" && buf != "*arcs"){
    cout << endl << "Number of nodes not matching, exiting" << endl;
    exit(-1);
  }
  
  network.Nlinks = 0;
  int NdoubleLinks = 0;
  int NselfLinks = 0;

	//map<int,map<int,double> > Links;
  
  // Read links in format "from to weight", for example "1 3 0.7"
  while(getline(net,line) != NULL){
    ss.clear();
    ss.str(line);
    ss >> buf;
    int linkEnd1 = atoi(buf.c_str());
    ss >> buf;
    int linkEnd2 = atoi(buf.c_str());
    buf.clear();
    ss >> buf;
    double linkWeight;
    if(buf.empty()) // If no information 
      linkWeight = 1.0;
    else
      linkWeight = atof(buf.c_str());
    linkEnd1--; // Nodes start at 1, but C++ arrays at 0.
    linkEnd2--;
    
		if(linkEnd2 < linkEnd1){
      int tmp = linkEnd1;
      linkEnd1 = linkEnd2;
      linkEnd2 = tmp;
    }
    
    if(linkEnd2 != linkEnd1){
      // Aggregate link weights if they are definied more than once
      map<int,map<int,double> >::iterator fromLink_it = network.Links.find(linkEnd1);
      if(fromLink_it == network.Links.end()){ // new link
        map<int,double> toLink;
        toLink.insert(make_pair(linkEnd2,linkWeight));
        network.Links.insert(make_pair(linkEnd1,toLink));
        network.Nlinks++;
      }
      else{
        map<int,double>::iterator toLink_it = fromLink_it->second.find(linkEnd2);
        if(toLink_it == fromLink_it->second.end()){ // new link
          fromLink_it->second.insert(make_pair(linkEnd2,linkWeight));
          network.Nlinks++;
        }
        else{
          toLink_it->second += linkWeight;
          NdoubleLinks++;
        }
      }
    }
    else{
      NselfLinks++;
    }
  }
  net.close();
  
  cout << "done! (found " << network.Nnode << " nodes and " << network.Nlinks << " links";
  if(NdoubleLinks > 0)
    cout << ", aggregated " << NdoubleLinks << " link(s) defined more than once";
  if(NselfLinks > 0)
    cout << ", ignoring " <<  NselfLinks << " self link(s)." << endl;
  else
    cout << ")" << endl;

}

  





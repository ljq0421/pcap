package org.fkjava.mavenqs;

import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import javax.websocket.*;
import javax.websocket.server.ServerEndpoint;
import java.io.*;
import java.util.concurrent.CopyOnWriteArraySet;

@Service
@ServerEndpoint(value = "/define")
@Component
public class HelloServiceImpl{// implements HelloService {

    //静态变量，用来记录当前在线连接数。应该把它设计成线程安全的。
    private static int onlineCount = 0;
    private static int messageCount=0;
    private static String[][] require=new String[200][255];
    //concurrent包的线程安全Set，用来存放每个客户端对应的MyWebSocket对象。
    private static CopyOnWriteArraySet<HelloServiceImpl> webSocketSet = new CopyOnWriteArraySet<HelloServiceImpl>();

    //与某个客户端的连接会话，需要通过它来给客户端发送数据
    private Session session;
    private static int messagenum=0;

    /**
     * 连接建立成功调用的方法*/
    @OnOpen
    public void onOpen(Session session) {
        this.session = session;
        webSocketSet.add(this);     //加入set中
        addOnlineCount();           //在线数加1
        resetMessageCount();
        System.out.println("define 有新连接加入！当前在线人数为" + getOnlineCount());
        try {
            sendMessage("Hello,you are NO."+getOnlineCount());
        } catch (IOException e) {
            System.out.println("IO异常");
        }
    }

    /**
     * 连接关闭调用的方法
     */
    @OnClose
    public void onClose() {
        webSocketSet.remove(this);  //从set中删除
        subOnlineCount();           //在线数减1
        System.out.println("define 有一连接关闭！当前在线人数为" + getOnlineCount());
    }

    /**
     * 收到客户端消息后调用的方法
     *
     * @param message 客户端发送过来的消息*/
    @OnMessage
    public void onMessage(String message, Session session) throws Exception {
        System.out.println("define 来自客户端的消息:" + message);
        require[onlineCount][messageCount]=message;
        addMessageCount();
        if(message.equals("index-warning")) {
            Process process0 = Runtime.getRuntime().exec("python /root/pcap/getrule.py " + require[onlineCount][6] );
            System.out.println("python /root/pcap/getrule.py " + require[onlineCount][6]);
            String COMMAND = "python /root/pcap/indexwarning.py ";
            try{
                String line=null;
                try {
                    Process process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][0] + " "+require[onlineCount][1] + " " +require[onlineCount][3]+ " " +require[onlineCount][4]+ " " +require[onlineCount][5]);
                    System.out.println(COMMAND + require[onlineCount][0] + " "+require[onlineCount][1] + " " +require[onlineCount][3]+ " " +require[onlineCount][4]+ " " +require[onlineCount][5]);
                    InputStream is = process.getInputStream();
                    InputStreamReader isr = new InputStreamReader(is);
                    BufferedReader br = new BufferedReader(isr);
                    while ((line = br.readLine()) != null) {
                        System.out.println(line);
                        System.out.flush();
                        sendMessage("require"+onlineCount+" "+messageCount+" "+line);
                    }
                    isr.close();
                    br.close();
                    is.close();
                }catch (Exception e){
                    e.printStackTrace();
                }
            }catch (Exception e){
                e.printStackTrace();
            }
            messagenum = 6;//规则名称、作用对象、报警类型（指标）、指标报警类型、符号（大于等）、数字
        }
        else if(message.equals("incident-warning")) {//报警类型最后发送
            if (require[onlineCount][0].equals("incident-ssh")) {//事件报警-ssh
                String COMMAND = "python /root/pcap/incidentwarning.py ";    // 要执行的语句，参数：rulename\ruleobject\incidenttype\sshsip\sshdip\sshport\sshdir\sshtype
                try {
                    try {
                        Process process;
                        if (require[onlineCount][8].equals("incident-warning")) {//没有高级定制
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7]);
                            System.out.println(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7]);
                        } else{//有高级定制
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7]+ " " + require[onlineCount][8] + " " + require[onlineCount][9]);
                            System.out.println(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7]+ " " + require[onlineCount][8] + " " + require[onlineCount][9]);
                        }
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                BufferedReader br = new BufferedReader(
                                        new InputStreamReader(process.getInputStream()));
                                try {
                                    while (br.readLine() != null)
                                        ;
                                    br.close();
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                            }
                        }).start();
                        BufferedReader br = null;
                        br = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                        String line = null;
                        while ((line = br.readLine()) != null) {
                            System.out.println(line);
                        }
                        process.waitFor();
                        br.close();
                        process.destroy();
                    }catch(Exception e) {
                            e.printStackTrace();
                    }
                } catch (Exception e) {
                        e.printStackTrace();
                }
            }
            else if (require[onlineCount][0].equals("incident-db")) {//事件报警-db
                String COMMAND = "python /root/pcap/incidentwarning.py ";    // 要执行的语句，参数：rulename\ruleobject\incidenttype\dbsip\dbdip\dbport\dbdir\dbtype\dbstate
                try {
                    try {
                        Process process;
                        if (require[onlineCount][9].equals("incident-warning")) {//没有高级定制
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7] + " " + require[onlineCount][8]);
                            System.out.println(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7] + " " + require[onlineCount][8]);
                        }else{
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7] + " " + require[onlineCount][8] + " " + require[onlineCount][9] + " " + require[onlineCount][10]);
                            System.out.println(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7] + " " + require[onlineCount][8] + " " + require[onlineCount][9] + " " + require[onlineCount][10]);
                        }
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                BufferedReader br = new BufferedReader(
                                        new InputStreamReader(process.getInputStream()));
                                try {
                                    while (br.readLine() != null)
                                        ;
                                    br.close();
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                            }
                        }).start();
                        BufferedReader br = null;
                        br = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                        String line = null;
                        while ((line = br.readLine()) != null) {
                            System.out.println(line);
                        }
                        process.waitFor();
                        br.close();
                        process.destroy();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            else if (require[onlineCount][0].equals("incident-scan")) {//事件报警-scan
                String COMMAND = "python /root/pcap/incidentwarning.py ";    // 要执行的语句，参数：rulename\ruleobject\incidenttype\scansip\scandip\scanport\scandir\scantype
                try {
                    try {
                        Process process;
                        if (require[onlineCount][8].equals("incident-warning")) {//没有高级定制
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7]);
                            System.out.println(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7]);
                        }else {
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7] + " " + require[onlineCount][8] + " " + require[onlineCount][9]);
                            System.out.println(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5] + " " + require[onlineCount][6] + " " + require[onlineCount][7] + " " + require[onlineCount][8] + " " + require[onlineCount][9]);
                        }
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                BufferedReader br = new BufferedReader(
                                        new InputStreamReader(process.getInputStream()));
                                try {
                                    while (br.readLine() != null)
                                        ;
                                    br.close();
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                            }
                        }).start();
                        BufferedReader br = null;
                        br = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                        String line = null;
                        while ((line = br.readLine()) != null) {
                            System.out.println(line);
                        }
                        process.waitFor();
                        br.close();
                        process.destroy();
                    }catch (Exception e) {
                        e.printStackTrace();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            else if (require[onlineCount][0].equals("incident-dos")) {//事件报警-dos
                String COMMAND = "python /root/pcap/incidentwarning.py ";    // 要执行的语句，参数：rulename\ruleobject\incidenttype\dostype
                try {
                    try {
                        Process process;
                        if (require[onlineCount][4].equals("incident-warning")) {//没有高级定制
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3]);
                            System.out.println(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3]);
                        } else {
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5]);
                            System.out.println(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5]);
                        }
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                BufferedReader br = new BufferedReader(
                                        new InputStreamReader(process.getInputStream()));
                                try {
                                    while (br.readLine() != null)
                                        ;
                                    br.close();
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                            }
                        }).start();
                        BufferedReader br = null;
                        br = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                        String line = null;
                        while ((line = br.readLine()) != null) {
                            System.out.println(line);
                        }
                        process.waitFor();
                        br.close();
                        process.destroy();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }catch (Exception e) {
                        e.printStackTrace();
                }
            }
            else if (require[onlineCount][0].equals("incident-ftp")) {//事件报警-ftp
                String COMMAND = "python /root/pcap/incidentwarning.py ";    // 要执行的语句，参数：rulename\ruleobject\incidenttype\sip\dip\port\dir\ftptype\ftptypee
                try {
                    try {//接收到的：incident-ftp、rulename、ruleobject、sip、dip、port、dir、type、typee、
                        Process process;
                        if (require[onlineCount][9].equals("incident-warning")) {//没有高级定制
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3]+ " " + require[onlineCount][4]+ " " + require[onlineCount][5]+ " " + require[onlineCount][6]+ " " + require[onlineCount][7]+ " " + require[onlineCount][8]);
                            System.out.println("success1:"+COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3]+ " " + require[onlineCount][4]+ " " + require[onlineCount][5]+ " " + require[onlineCount][6]+ " " + require[onlineCount][7]+ " " + require[onlineCount][8]);
                        }else{
                            process = Runtime.getRuntime().exec(COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3]+ " " + require[onlineCount][4] + " " + require[onlineCount][5]+ " " + require[onlineCount][6]+ " " + require[onlineCount][7]+ " " + require[onlineCount][8]+ " " + require[onlineCount][9]+ " " + require[onlineCount][10] );
                            System.out.println("success2:"+COMMAND + require[onlineCount][1] + " " + require[onlineCount][2] + " " + require[onlineCount][0] + " " + require[onlineCount][3] + " " + require[onlineCount][4] + " " + require[onlineCount][5]+ " " + require[onlineCount][6]+ " " + require[onlineCount][7]+ " " + require[onlineCount][8]+ " " + require[onlineCount][9]+ " " + require[onlineCount][10]);
                        }
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                BufferedReader br = new BufferedReader(
                                        new InputStreamReader(process.getInputStream()));
                                try {
                                    while (br.readLine() != null)
                                        ;
                                    br.close();
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                            }
                        }).start();
                        BufferedReader br = null;
                        br = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                        String line = null;
                        while ((line = br.readLine()) != null) {
                            System.out.println(line);
                        }
                        process.waitFor();
                        br.close();
                        process.destroy();
                    }catch (Exception e) {
                        e.printStackTrace();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
    /**
     * 发生错误时调用*/
     @OnError
     public void onError(Session session, Throwable error) {
        System.out.println("发生错误");
        error.printStackTrace();
     }

     public void sendMessage(String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
     }

     /**
      * 群发自定义消息
      * */
    public static void sendInfo(String message) throws IOException {
        for (HelloServiceImpl item : webSocketSet) {
            try {
                item.sendMessage(message);
            } catch (IOException e) {
                continue;
            }
        }
    }


    public static synchronized int getOnlineCount() {
        return onlineCount;
    }

    public static synchronized void addOnlineCount() {
        HelloServiceImpl.onlineCount++;
    }

    public static synchronized void subOnlineCount() {
        HelloServiceImpl.onlineCount--;
    }

    public static synchronized void resetMessageCount() {
        messageCount=0;
    }

    public static synchronized void addMessageCount() {
        HelloServiceImpl.messageCount++;
    }

}

